from pyalgotrade import plotter

from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade.stratanalyzer import returns
from pyalgotrade.stratanalyzer import drawdown
from pyalgotrade.stratanalyzer import trades

from pyalgotrade.barfeed import yahoofeed
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

import StrategyUtil

def main(plot):
    # Load  bar feed from CSV file/Yahoo format
    feed = yahoofeed.Feed()

    instrument = "n225"
    feed.addBarsFromCSV(instrument, r".\Data\n225.csv")

    #instrument = "hsi"
    #feed.addBarsFromCSV(instrument, r".\Data\hsi.csv")

    # instrument = "hsce"
    # feed.addBarsFromCSV(instrument, r".\Data\hsce.csv")

    # instrument = "tsec"
    # feed.addBarsFromCSV(instrument, r".\Data\tsec.csv")

    # instrument = "asx"
    # feed.addBarsFromCSV(instrument, r".\Data\asx.csv")

    # instrument = "kospi"
    # feed.addBarsFromCSV(instrument, r".\Data\kospi.csv")

    #instrument = "nifty"
    #feed.addBarsFromCSV(instrument, r".\Data\nifty.csv")

    #instrument = "jkse"
    #feed.addBarsFromCSV(instrument, r".\Data\jkse.csv")

    # parameters
    hurstPeriod = 100

    macdShorterPeriod = 12
    macdLongerPeriod = 36
    macdSignalPeriod = 9

    entrySMAPeriod = 65
    exitSMAPeriod = 4
    rsiPeriod = 2
    overBoughtThreshold = 80
    overSoldThreshold = 20

    strategy = StrategyUtil.ComprehensiveStrategy(feed, instrument, hurstPeriod, macdShorterPeriod, macdLongerPeriod, macdSignalPeriod, rsiPeriod, entrySMAPeriod, exitSMAPeriod, overBoughtThreshold, overSoldThreshold)

    #Attach a Sharpe Ratio analyser
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strategy.attachAnalyzer(sharpeRatioAnalyzer)

    #Attach a Drawdown analyzer
    drawdownAnalyzer = drawdown.DrawDown()
    strategy.attachAnalyzer(drawdownAnalyzer)

    # Attach a return analyzer
    returnsAnalyzer = returns.Returns()
    strategy.attachAnalyzer(returnsAnalyzer)

    # Attach trade analyzer
    tradesAnalyzer = trades.Trades()
    strategy.attachAnalyzer(tradesAnalyzer)

    if plot:
        plt = plotter.StrategyPlotter(strategy, True, False, True)
        plt.getOrCreateSubplot("hurst").addDataSeries("Hurst", strategy.getHurst())
        plt.getOrCreateSubplot("hurst").addLine("Random", 0.5)

        # Plot the simple returns on each bar.
        plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    strategy.run()
    strategy.info("Final portfolio value: $%.2f" % strategy.getResult())
    print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))
    print("Maximum Drawdown : %.2f" % drawdownAnalyzer.getMaxDrawDown())
    print("Longest Drawdown Duration : %s" % drawdownAnalyzer.getLongestDrawDownDuration())
    print("Cumulative returns: %.2f %%" % (returnsAnalyzer.getCumulativeReturns()[-1] * 100))

    print("")
    print("Total trades: %d" % (tradesAnalyzer.getCount()))
    if tradesAnalyzer.getCount() > 0:
        profits = tradesAnalyzer.getAll()
        print("Avg. profit: $%2.f" % (profits.mean()))
        print("Profits std. dev.: $%2.f" % (profits.std()))
        print("Max. profit: $%2.f" % (profits.max()))
        print("Min. profit: $%2.f" % (profits.min()))
        tradeAnalyzerAllReturns = tradesAnalyzer.getAllReturns()
        print("Avg. return: %2.f %%" % (tradeAnalyzerAllReturns.mean() * 100))
        print("Returns std. dev.: %2.f %%" % (tradeAnalyzerAllReturns.std() * 100))
        print("Max. return: %2.f %%" % (tradeAnalyzerAllReturns.max() * 100))
        print("Min. return: %2.f %%" % (tradeAnalyzerAllReturns.min() * 100))

    print("")
    print("Profitable trades: %d" % (tradesAnalyzer.getProfitableCount()))
    if tradesAnalyzer.getProfitableCount() > 0:
        profits = tradesAnalyzer.getProfits()
        print("Avg. profit: $%2.f" % (profits.mean()))
        print("Profits std. dev.: $%2.f" % (profits.std()))
        print("Max. profit: $%2.f" % (profits.max()))
        print("Min. profit: $%2.f" % (profits.min()))
        tradeAnalyzerPositiveReturns = tradesAnalyzer.getPositiveReturns()
        print("Avg. return: %2.f %%" % (tradeAnalyzerPositiveReturns.mean() * 100))
        print("Returns std. dev.: %2.f %%" % (tradeAnalyzerPositiveReturns.std() * 100))
        print("Max. return: %2.f %%" % (tradeAnalyzerPositiveReturns.max() * 100))
        print("Min. return: %2.f %%" % (tradeAnalyzerPositiveReturns.min() * 100))

    print("")
    print("Unprofitable trades: %d" % (tradesAnalyzer.getUnprofitableCount()))
    if tradesAnalyzer.getUnprofitableCount() > 0:
        losses = tradesAnalyzer.getLosses()
        print("Avg. loss: $%2.f" % (losses.mean()))
        print("Losses std. dev.: $%2.f" % (losses.std()))
        print("Max. loss: $%2.f" % (losses.min()))
        print("Min. loss: $%2.f" % (losses.max()))
        tradeAnalyzerNegativeReturns = tradesAnalyzer.getNegativeReturns()
        print("Avg. return: %2.f %%" % (tradeAnalyzerNegativeReturns.mean() * 100))
        print("Returns std. dev.: %2.f %%" % (tradeAnalyzerNegativeReturns.std() * 100))
        print("Max. return: %2.f %%" % (tradeAnalyzerNegativeReturns.max() * 100))
        print("Min. return: %2.f %%" % (tradeAnalyzerNegativeReturns.min() * 100))

    if plot:
        plt.plot()

if __name__ == "__main__":
    main(True)
