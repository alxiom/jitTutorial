/**
  * Created by Alex on 02/02/2019.
  */

import colossus.core.ServerContext
import colossus.protocols.http.HttpMethod._
import colossus.protocols.http.UrlParsing._
import colossus.protocols.http._
import colossus.service.Callback
import colossus.service.GenRequestHandler.PartialHandler
import javax.inject.{Inject, Singleton}

@Singleton
class HandleRequest @Inject()(context: ServerContext,
                              evalJNI: EvalJNI,
                              pModel: Long,
                              calculateRequest: CalculateRequest) extends RequestHandler(context) {

  private val log = com.typesafe.scalalogging.Logger(getClass)
  private val jsonHeader = HttpHeader("Content-type", "application/json")

  private val regexPostId = "[\\-\\d]{16,}".r
  private val regexPostMessage = "Content-Disposition: form-data; name=\"([a-zA-Z0-9]+)\"".r

  def parsePostRequest(text: String): Map[String, String] = {
    val removePostId = regexPostId.replaceAllIn(text, "").replaceAll("\r|\n", "")
    val extractPostMessage = regexPostMessage.replaceAllIn(removePostId, y => s"\u241D${y.group(1)}\u241E").drop(1)
    val extractKeyValueMap = extractPostMessage.split("\u241D").map(x => {
      val s = x.split("\u241E")
      (s(0), s(1))
    }).toMap
    extractKeyValueMap
  }

  override def handle: PartialHandler[Http] = {
    case req @ Get on Root =>
      log.info(s"aliveCheck=200")
      Callback.successful(req.ok("""{"status": "ok", "code": 200}""", HttpHeaders(jsonHeader)))
    case req @ Get on Root / "model" / "bsf" =>
      val parametersMap = req.head.parameters.parameters.toMap
      val queryO = parametersMap.get("q")
      if (queryO.nonEmpty) {
        val result = calculateRequest(queryO.get, evalJNI, pModel)
        val responseJson = s"""{"status": "ok", "code": 200, "data": {"result": ${result}}}"""
        Callback.successful(req.ok(responseJson, HttpHeaders(jsonHeader)))
      } else {
        val emptyQueryErrorJson = """{"status": "error", "code": 400, "message": "empty query"}"""
        Callback.successful(req.badRequest(emptyQueryErrorJson, HttpHeaders(jsonHeader)))
      }
    case req @ Post on Root / "model" / "bsf" =>
      val bytes = req.body.bytes
      if (bytes.isEmpty) {
        val emptyBodyErrorJson = """{"status": "error", "code": 400, "message": "missing body"}"""
        Callback.successful(req.badRequest(emptyBodyErrorJson, HttpHeaders(jsonHeader)))
      } else {
        val body = bytes.utf8String
        val requestMap = parsePostRequest(body) // TODO: Post Request should contain key "query"
        val result = calculateRequest(requestMap("query"), evalJNI, pModel)
        val responseJson = s"""{"status": "ok", "code": 200, "data": {"result": "${result}"}}"""
        Callback.successful(req.ok(responseJson, HttpHeaders(jsonHeader)))
      }
  }

}
