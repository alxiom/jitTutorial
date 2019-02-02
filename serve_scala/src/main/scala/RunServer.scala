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
  val calculateRequest: CalculateRequest = injector.getInstance(classOf[CalculateRequest])

  def main(args: Array[String]): Unit = {
    println(s"serverStart=${System.currentTimeMillis()}")
    log.info(s"serverStart=${System.currentTimeMillis()}")

    val pModel: Long = evalJNI.loadModel(s"${projectPath}/src/main/resources/trace_model.pth")
    log.info(s"modelPointer=${pModel}")

    HttpServer.start("PyTorchModelServer", 9000){initContext =>
      new Initializer(initContext) {
        override def onConnect: RequestHandlerFactory = serverContext => {
          new HandleRequest(serverContext, evalJNI, pModel, calculateRequest)
        }
      }
    }
  }

}
