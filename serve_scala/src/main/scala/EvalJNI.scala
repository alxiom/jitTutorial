/**
  * Created by alex on 15/01/2019
  */

class EvalJNI {

  @native def loadModel(modelName: String): Long
  @native def evaluate(pModel: Long, x: Array[Float]): Array[Float]

}

object EvalJNI {

  def main(args: Array[String]): Unit = {
    val projectPath = System.getProperty("user.dir")
    System.load(s"${projectPath}/lib/libModel.dylib")

    val x = Array(1.0F, 1.0F, 1.0F)
    val eval = new EvalJNI
    val pModel = eval.loadModel(s"${projectPath}/src/main/resources/trace_model.pth")
    val prediction = eval.evaluate(pModel, x)

    println(s"model pointer: ${pModel}")
    println(s"prediction: ${prediction.mkString(",")}")
  }

}
