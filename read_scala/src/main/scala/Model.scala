/**
  * Created by alex on 15/01/2019
  */

class Model {
  // --- Native methods
  @native def intMethod(n: Int): Int
  @native def booleanMethod(b: Boolean): Boolean
  @native def stringMethod(s: String): String
  @native def intArrayMethod(a: Array[Int]): Int
  @native def doubleArrayMethod(a: Array[Double]): Int
  @native def floatArrayMethod(a: Array[Float]): Int
}

// --- Code in App body will get wrapped in a main method on compilation
object Model extends App {

  // --- Main method to test our native library
  System.loadLibrary("Model")
  val model = new Model
  val square = model.intMethod(5)
  val bool = model.booleanMethod(true)
  val text = model.stringMethod("java")
  val sum = model.intArrayMethod(Array(1, 1, 2, 3, 5, 8, 13))

  println(s"intMethod: $square")
  println(s"booleanMethod: $bool")
  println(s"stringMethod: $text")
  println(s"intArrayMethod: $sum")
}
