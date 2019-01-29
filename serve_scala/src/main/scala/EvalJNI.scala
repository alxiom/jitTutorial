/**
  * Created by alex on 15/01/2019
  */

import com.google.inject.{Guice, Injector}
import javax.inject.Singleton

@Singleton
class EvalJNI {

  @native def loadModel(modelName: String): Long
  @native def evaluate(pModel: Long, x: Array[Float]): Array[Float]

}

object EvalJNI {

  val projectPath: String = System.getProperty("user.dir")
  System.load(s"${projectPath}/lib/libModel.dylib")

  val injector: Injector = Guice.createInjector()
  val evalJNI: EvalJNI = injector.getInstance(classOf[EvalJNI])

  def main(args: Array[String]): Unit = {
    val x = (1 to 3).toArray.map(i => i.toFloat)
    val pModel: Long = evalJNI.loadModel(s"${projectPath}/src/main/resources/trace_model.pth")
    (1 to 100).foreach(_ => {
      val st = System.currentTimeMillis()
      val prediction = evalJNI.evaluate(pModel, x)
      println(s"${System.currentTimeMillis() - st} prediction: ${prediction.mkString(",")}")
    })
  }

}
