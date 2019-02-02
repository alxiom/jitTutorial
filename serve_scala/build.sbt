name := "read_scala"

version := "0.1"

scalaVersion := "2.12.4"

val javaxV = "1"
val guiceV = "4.0"
val akkaV = "2.5.17"
val colossusV = "0.11.0"
val loggerV = "3.9.0"
val logbackV = "1.2.3"

libraryDependencies ++= Seq(
  "javax.inject" % "javax.inject" % javaxV,
  "com.google.inject" % "guice" % guiceV,
  "com.typesafe.akka" %% "akka-actor" % akkaV,
  "com.tumblr" %% "colossus" % colossusV,
  "com.typesafe.scala-logging" %% "scala-logging" % loggerV,
  "ch.qos.logback" % "logback-classic" % logbackV
)