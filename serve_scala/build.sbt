name := "read_scala"

version := "0.1"

scalaVersion := "2.12.4"

val javaxV = "1"
val guiceV = "4.0"

libraryDependencies ++= Seq(
  "javax.inject" % "javax.inject" % javaxV,
  "com.google.inject" % "guice" % guiceV
)