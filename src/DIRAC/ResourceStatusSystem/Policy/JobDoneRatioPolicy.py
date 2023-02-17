""" JobDoneRatioPolicy

  Policy that calculates the efficiency following the formula::

    done / ( completed + done )

  if the denominator is smaller than 10, it does not take any decision.

"""
from DIRAC import S_OK
from DIRAC.ResourceStatusSystem.PolicySystem.PolicyBase import PolicyBase


class JobDoneRatioPolicy(PolicyBase):
    """
    The JobEfficiencyPolicy class is a policy that checks the efficiency of the
    jobs according to what is on JobDB.

      Evaluates the JobDoneRatioPolicy results given by the JobCommand.JobCommand
    """

    @staticmethod
    def _evaluate(commandResult):
        """_evaluate

        efficiency < 0.5 :: Banned
        efficiency < 0.9 :: Degraded

        """

        result = {"Status": None, "Reason": None}

        if not commandResult["OK"]:
            result["Status"] = "Error"
            result["Reason"] = commandResult["Message"]
            return S_OK(result)

        commandResult = commandResult["Value"]

        if not commandResult:
            result["Status"] = "Unknown"
            result["Reason"] = "No values to take a decision"
            return S_OK(result)

        commandResult = commandResult[0]

        if not commandResult:
            result["Status"] = "Unknown"
            result["Reason"] = "No values to take a decision"
            return S_OK(result)

        completed = commandResult["Completed"]
        done = commandResult["Done"]

        total = completed + done

        # we want a minimum amount of jobs to take a decision ( at least 10 pilots )
        if total < 10:
            result["Status"] = "Unknown"
            result["Reason"] = "Not enough jobs to take a decision"
            return S_OK(result)

        efficiency = done / total

        if efficiency <= 0.5:
            result["Status"] = "Banned"
        elif efficiency <= 0.9:
            result["Status"] = "Degraded"
        else:
            result["Status"] = "Active"

        result["Reason"] = f"Job Done ratio of {efficiency:.2f}"
        return S_OK(result)
