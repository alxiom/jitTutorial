/**
  * Created by alex on 15/01/2019
  */

class ModelJNI {
  // --- Native methods
  @native def floatArrayMethod(a: Array[Float]):Array[Float]
}

// --- Code in App body will get wrapped in a main method on compilation
object ModelJNI extends App {

  // --- Main method to test our native library
  System.loadLibrary("ModelJNI")
  val model = new ModelJNI
  val prediction = model.floatArrayMethod(Array(1.0F, 1.0F, 1.0F))

  println(s"floatArrayMethod: $prediction")
}
