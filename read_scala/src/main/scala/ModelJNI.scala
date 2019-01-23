/**
  * Created by alex on 15/01/2019
  */

class ModelJNI {
  // --- Native methods
  @native def floatArrayMethod(x: Array[Float]):Array[Float]

}

// --- Code in App body will get wrapped in a main method on compilation
object ModelJNI extends App {

  // --- Main method to test our native library

//  System.setProperty("java.library.path", "/Users/alex/git/jitTutorial/read_scala/lib")
//  System.loadLibrary("ModelJNI")

  System.load("/Users/alex/git/jitTutorial/read_scala/lib/libModelJNI.so")

  val model = new ModelJNI
  val prediction = model.floatArrayMethod(Array(1.0F, 1.3F, 1.0F))

  println(s"floatArrayMethod: ${prediction.mkString(",")}")
}
