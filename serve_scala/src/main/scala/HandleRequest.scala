/**
  * Created by Alex on 02/02/2019.
  */

import colossus.core.ServerContext
import colossus.protocols.http.HttpMethod._
import colossus.protocols.http.UrlParsing._
import colossus.protocols.http.{Http, HttpHeader, HttpHeaders, RequestHandler}
import colossus.service.Callback
import colossus.service.GenRequestHandler.PartialHandler
import javax.inject.{Inject, Singleton}

@Singleton
class HandleRequest @Inject()(context: ServerContext, evalJNI: EvalJNI, pModel: Long) extends RequestHandler(context) {

  private val log = com.typesafe.scalalogging.Logger(getClass)
  private val inputTypes = Array("bf", "bsf")
  private val jsonHeader = HttpHeader("Content-type", "application/json")

  override def handle: PartialHandler[Http] = {
    case req @ Get on Root =>
      log.info(s"aliveCheck=200")
      Callback.successful(req.ok("""{"status": "ok", "code": 200}""", HttpHeaders(jsonHeader)))
    case req @ Get on Root / "model" =>
      val parametersMap = req.head.parameters.parameters.toMap
      val queryO = parametersMap.get("type")
      if (queryO.nonEmpty) {
        val isAvailable = inputTypes.contains(queryO.get)
        val responseJson = s"""{"status": "ok", "code": 200, "data": {"isAvailable": ${isAvailable}}}"""
        Callback.successful(req.ok(responseJson, HttpHeaders(jsonHeader)))
      } else {
        val emptyQueryErrorJson = """{"status": "error", "code": 400, "message": "empty-query"}"""
        Callback.successful(req.badRequest(emptyQueryErrorJson, HttpHeaders(jsonHeader)))
      }
    case req @ Post on Root / "model" / "bsf" =>
      val bytes = req.body.bytes
      if (bytes.isEmpty) {
        val emptyBodyErrorJson = """{"status": "error", "code": 400, "message": "missing body"}"""
        Callback.successful(req.badRequest(emptyBodyErrorJson, HttpHeaders(jsonHeader)))
      } else {
        val responseJson = s"""{"status": "ok", "code": 200, "data": {"isAvailable": ${bytes.utf8String}}}"""
        Callback.successful(req.ok(responseJson, HttpHeaders(jsonHeader)))
      }
  }

}
