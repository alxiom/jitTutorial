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

  private val port: Int = System.getProperty("port", "9000").toInt
  private val inputDim: Long = System.getProperty("input_dim", "35").toLong
  private val projectPath: String = System.getProperty("user.dir")
  System.load(s"${projectPath}/lib/libModel.dylib")

  private val injector: Injector = Guice.createInjector()
  private val runEval: RunEval = injector.getInstance(classOf[RunEval])
  private val evalJNI: EvalJNI = injector.getInstance(classOf[EvalJNI])
  private val modelP: Long = evalJNI.loadModel(s"${projectPath}/src/main/resources/trace_model.pth")

  def main(args: Array[String]): Unit = {
    println(s"serverStart\u241Btimestamp=${System.currentTimeMillis()}\u241BmodelPointer=${modelP}")

    HttpServer.start("PyTorchModelServer", port){initContext =>
      new Initializer(initContext) {
        override def onConnect: RequestHandlerFactory = serverContext => {
          new ManageRequest(serverContext, inputDim, runEval, modelP)
        }
      }
    }
  }

}