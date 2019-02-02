/**
  * Created by Alex on 02/02/2019.
  */

import akka.actor.ActorSystem
import colossus.core.IOSystem
import colossus.protocols.http.{HttpServer, Initializer}
import com.google.inject.{Guice, Injector}

object RunServer {

  implicit val actorSystem: ActorSystem = ActorSystem()
  implicit val ioSystem: IOSystem = IOSystem()
  private val log = com.typesafe.scalalogging.Logger(getClass)

  val projectPath: String = System.getProperty("user.dir")
  System.load(s"${projectPath}/lib/libModel.dylib")

  val injector: Injector = Guice.createInjector()
  val evalJNI: EvalJNI = injector.getInstance(classOf[EvalJNI])

  def main(args: Array[String]): Unit = {
    println(s"serverStart=${System.currentTimeMillis()}")
    log.info(s"serverStart=${System.currentTimeMillis()}")

    val pModel: Long = evalJNI.loadModel(s"${projectPath}/src/main/resources/trace_model.pth")
    log.info(s"modelPointer=${pModel}")

    HttpServer.start("PyTorchModelServer", 9000){initContext =>
      new Initializer(initContext) {
        override def onConnect: RequestHandlerFactory = serverContext => {
          new HandleRequest(serverContext, evalJNI, pModel)
        }
      }
    }
  }

}

//class ServerRequestHandler @Inject()(context: ServerContext, evalJNI: EvalJNI, pModel: Long) extends RequestHandler(context) {
//
//  override def handle: PartialHandler[Http] = {
//    case req @ Get on Root =>
//      Callback.successful(req.ok("""{"status": "ok", "code": 200}""", HttpHeaders(HttpHeader("Content-type", "application/json"))))
//    case req @ Get on Root / "chat" / "cloud" =>
//      val parametersMap = req.head.parameters.parameters.toMap
//      val queryO = parametersMap.get("q")
//      if (queryO.nonEmpty) {
//        val answer = evalJNI()
//        val answerJson =
//          s"""
//             |{
//             |  "status": "ok",
//             |  "code": 200,
//             |  "data": {
//             |    "answer": "${answer}"
//             |  }
//             |}
//           """.stripMargin
//        Callback.successful(req.ok(answerJson, HttpHeaders(HttpHeader("Content-type", "application/json"))))
//      } else {
//        Callback.successful(req.badRequest("""{"status": "error", "code": 400, "message": "empty-query"}""", HttpHeaders(HttpHeader("Content-type", "application/json"))))
//      }
//  }
//
//}