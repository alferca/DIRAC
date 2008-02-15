# $Header: /tmp/libdirac/tmp.stZoy15380/dirac/DIRAC3/DIRAC/AccountingSystem/Service/ReportGeneratorHandler.py,v 1.1 2008/02/15 17:17:15 acasajus Exp $
__RCSID__ = "$Id: ReportGeneratorHandler.py,v 1.1 2008/02/15 17:17:15 acasajus Exp $"
import types
from DIRAC import S_OK, S_ERROR
from DIRAC.AccountingSystem.private.AccountingDB import AccountingDB
from DIRAC.AccountingSystem.private.Summaries import Summaries
from DIRAC.Core.DISET.RequestHandler import RequestHandler
from DIRAC.Core.Utilities import Time

gAccountingDB = False

def initializeReportGeneratorHandler( serviceInfo ):
  global gAccountingDB
  gAccountingDB = AccountingDB()
  return S_OK()

class ReportGeneratorHandler( RequestHandler ):

  types_generateSummary = [ types.StringType, Time._dateTimeType, Time._dateTimeType, types.DictType ]
  def export_generateSummary( self, summaryName, startTime, endTime, argsDict ):
    """
    Generate summaries
      Arguments:
        - summaryName : Name of summary (easy!)
        - startTime
        - endTime
        - argsDict : Arguments to the summary.
    """
    summariesGeneator = Summaries( gAccountingDB, self.serviceInfoDict[ 'clientSetup' ] )
    return summariesGeneator.generate( summaryName, startTime, endTime, argsDict )