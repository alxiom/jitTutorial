/**
  * Created by Alex on 03/02/2019.
  */

import javax.inject.Singleton

@Singleton
class CalculateRequest {

  private val log = com.typesafe.scalalogging.Logger(getClass)

  def apply(query: String, evalJNI: EvalJNI, pModel: Long): String = {
    val x = (1 to 35).toArray.map(i => i.toFloat) // TODO : preprocess query to generate x
    val prediction = evalJNI.evaluate(pModel, x)
    log.info(s"query=${query}\u241BmodelResult=${prediction.mkString(",")}")
    prediction.mkString(",")
  }

}
