enablePlugins(SbtJsEngine)

scalaVersion in Global := "2.11.8"

lazy val js = project

val indexHtml = taskKey[File]("Generate an index.html that follows TodoMVC's Application Specification")

indexHtml := {
  val linkedJs = (scalaJSLinkedFile in js in Compile).value.asInstanceOf[org.scalajs.core.tools.io.FileVirtualJSFile]
  val document = <html>
    <head>
      <title>Binding.scala • TodoMVC</title>
    </head>
    <body>
      <script type="text/javascript" src={ linkedJs.file.relativeTo(baseDirectory.value).get.toString }></script>
      <script type="text/javascript"> com.thoughtworks.todo.Main().main() </script>
    </body>
  </html>
  val outputFile = baseDirectory.value / "index.html"
  IO.writeLines(outputFile, Seq("<!DOCTYPE html>", xml.Xhtml.toXhtml(document)))
  outputFile
}
