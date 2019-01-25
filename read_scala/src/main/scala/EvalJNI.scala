/**
  * Created by alex on 15/01/2019
  */

class EvalJNI {

  @native def loadModel(modelName: String): Long
  @native def evaluate(pModel: Long, x: Array[Float]): Array[Float]

}

object EvalJNI {

  def main(args: Array[String]): Unit = {
    System.load("/Users/alex/git/jitTutorial/read_scala/lib/libModelJNI.so")
//    System.setProperty("java.library.path", "/Users/alex/git/jitTutorial/read_scala/lib")
//    System.loadLibrary("ModelJNI")

    val x = Array(1.0F, 1.0F, 2.0F)
    val eval = new EvalJNI
    val pModel = eval.loadModel("traced_model.pth")
    val prediction = eval.evaluate(pModel, x)

    println(s"model pointer: ${pModel}")
    println(s"prediction: ${prediction.mkString(",")}")
  }

}
