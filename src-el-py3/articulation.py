# Copyright (c) 2014 University of California, Davis
#
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import copy
import subprocess
from relations import *
from taxonomy2 import *
from helper2 import *

class Articulation:

    def __init__(self, initInput="", mapping=None):
        self.string = initInput
        self.numTaxon = 2
        self.confidence = 2
        self.relations = 0
        self.sumLabel = False
        if (initInput == ""):
            self.taxon1 = Taxon()
            self.taxon2 = Taxon()
            self.taxon3 = Taxon()
            self.taxon4 = Taxon()
            self.taxon5 = Taxon()
            return None

        # Parsing begins here
        if (initInput.find("confidence=") != -1):
            elements = re.match("(.*) confidence=(.*)", initInput)
            initInput = elements.group(1)
            self.confidence = int(elements.group(2))
        if (initInput.find("lsum ") != -1 or initInput.find("l3sum ") != -1 or\
            initInput.find("l4sum ") != -1 or initInput.find("rsum ") != -1 or\
            initInput.find("r3sum ") != -1 or initInput.find("r4sum ") != -1 or\
            initInput.find("ldiff ") != -1 or initInput.find("rdiff ") != -1 or
            initInput.find("e4sum") != -1 or initInput.find("i4sum") != -1):
            self.sumLabel = True
        if self.sumLabel:
            if (initInput.find("lsum") != -1):
                self.relations = relation["+="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) lsum (.*)\.(.*)", initInput)
            elif (initInput.find("l3sum") != -1):
                self.relations = relation["+3="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) (.*)\.(.*) l3sum (.*)\.(.*)", initInput)
            elif (initInput.find("l4sum") != -1):
                self.relations = relation["+4="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) (.*)\.(.*) (.*)\.(.*) l4sum (.*)\.(.*)", initInput)
            elif (initInput.find("rsum") != -1):
                self.relations = relation["=+"]
                elements = re.match("(.*)\.(.*) rsum (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("r3sum") != -1):
                self.relations = relation["=3+"]
                elements = re.match("(.*)\.(.*) r3sum (.*)\.(.*) (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("r4sum") != -1):
                self.relations = relation["=4+"]
                elements = re.match("(.*)\.(.*) r4sum (.*)\.(.*) (.*)\.(.*) (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("ldiff") != -1):
                self.relations = relation["-="]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) ldiff (.*)\.(.*)", initInput)
            elif (initInput.find("rdiff") != -1):
                self.relations = relation["=-"]
                elements = re.match("(.*)\.(.*) rdiff (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("e4sum") != -1):
                self.relations = 0 #[relationDict["+=+"]]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) e4sum (.*)\.(.*) (.*)\.(.*)", initInput)
            elif (initInput.find("i4sum") != -1):
                self.relations = 0 #[relationDict["+<=+"]]
                elements = re.match("(.*)\.(.*) (.*)\.(.*) i4sum (.*)\.(.*) (.*)\.(.*)", initInput)
            else:
                raise Exception("Syntax error in \""+initInput+"\"!!")

            taxon1taxonomy = elements.group(1).strip()
            taxon1taxon = elements.group(2).strip()
            taxon2taxonomy = elements.group(3).strip()
            taxon2taxon = elements.group(4).strip()
            taxon3taxonomy = elements.group(5).strip()
            taxon3taxon = elements.group(6).strip()
            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)
            self.taxon3 = mapping.getTaxon(taxon3taxonomy, taxon3taxon)
            self.numTaxon = 3
            if(initInput.find("e4sum") != -1 or initInput.find("i4sum") != -1 or initInput.find("l3sum") != -1 or initInput.find("r3sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
                self.numTaxon = 4
            if(initInput.find("l4sum") != -1 or initInput.find("r4sum") != -1):
                taxon4taxonomy = elements.group(7)
                taxon4taxon = elements.group(8)
                self.taxon4 = mapping.getTaxon(taxon4taxonomy, taxon4taxon)
                taxon5taxonomy = elements.group(9)
                taxon5taxon = elements.group(10)
                self.taxon5 = mapping.getTaxon(taxon5taxonomy, taxon5taxon)
                self.numTaxon = 5
        else:
            ## initInput is of form b48.a equals k04.a
            self.relation = 0
            if (initInput.find("{") != -1):
                elements = re.match("(.*)\.(\S*)\s*{(.*)}\s*(\S*)\.(.*)", initInput)
            else:
                elements = re.match("(.*)\.(\S*)\s*(\S*)\s*(\S*)\.(.*)", initInput)
            if elements is None:
                raise Exception("Syntax error in \""+initInput+"\"!!")

            taxon1taxonomy = elements.group(1).strip()
            taxon1taxon = elements.group(2).strip()
            relString = elements.group(3).strip()
            taxon2taxonomy = elements.group(4).strip()
            taxon2taxon = elements.group(5).strip()

            if (relString.find(" ") != -1):
                if (relString in relation):
                    self.relations = rcc5[relString]
                else:
                    relElements = re.split("\s+", relString)

                    for rel in relElements:
                        self.relations |= rcc5[rel]

            else:
                self.relations = rcc5[relString]

            self.taxon1 = mapping.getTaxon(taxon1taxonomy, taxon1taxon)
            self.taxon2 = mapping.getTaxon(taxon2taxonomy, taxon2taxon)

    def toRCCASP(self, align, rnr):
        name1 = self.taxon1.dlvName()
        name2 = self.taxon2.dlvName()
        relpreds = []
        if reasoner[rnr] == reasoner["rccdlv"]:
            disjunctive = " v "
        elif reasoner[rnr] == reasoner["rccclingo"]:
            disjunctive = " ; "
        result = ""

        if self.relations & rcc5["equals"]:
            relpreds.append("eq")
        if self.relations & rcc5["is_included_in"]:
            relpreds.append("pp")
        if self.relations & rcc5["includes"]:
            relpreds.append("pi")
        if self.relations & rcc5["disjoint"]:
            relpreds.append("dr")
        if self.relations & rcc5["overlaps"]:
            relpreds.append("po")

        for relpred in relpreds:
            result += relpred + "(" + name1 + ", " + name2 + ")"
            result += disjunctive

        result = result[:-3] + ".\n"
        return result

    def toShawnASP(self, align, rnr):
        name1 = self.taxon1.dlvName()
        name2 = self.taxon2.dlvName()
        relpreds = ""
#         if reasoner[rnr] == reasoner["rcctt"]:
#             disjunctive = " v "
#         elif reasoner[rnr] == reasoner["rccclingo"]:
#             disjunctive = " ; "
        result = ""

        # order : dr eq pi po pp
        if self.relations & rcc5["disjoint"]:
            relpreds += "dr"
        if self.relations & rcc5["equals"]:
            relpreds += "eq"
        if self.relations & rcc5["includes"]:
            relpreds += "pi"
        if self.relations & rcc5["overlaps"]:
            relpreds += "po"
        if self.relations & rcc5["is_included_in"]:
            relpreds += "pp"

        result = "r(" + relpreds + ", " + name1 + ", " + name2 + ").\n"
        return result

    def toASP(self, enc, rnr, align):
        result = ""
        name1 = self.taxon1.dlvName()
        name2 = self.taxon2.dlvName()
        disjointSymbol = "v" if reasoner[rnr] == reasoner["dlv"] else ";"
        twoPredFormat = ":- {}, {}.\n"
        threePredFormat = ":- {}, {}, {}.\n"

        if encode[enc] & encode["vr"] or encode[enc] & encode["dl"] or encode[enc] & encode["mn"]:
            if self.relations == rcc5["equals"]:
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- out3(" + name1 + ", X, R), in(" + name2 + ",X), ix.\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- in(" + name1 + ",X), out3(" + name2 + ", X, R), ix.\n"

                result += AggregationRule(firstVar=name1, secondVar=name2).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == rcc5["includes"]:
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X), pw.\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- out3(" + name1 + ", X, R), in(" + name2 + ",X), ix.\n"

                result += AggregationRule(firstVar=name1, secondVar=name2).rule
                result += AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == rcc5["is_included_in"]:

                result = AggregationRule(firstVar=name1, secondVar=name2).rule
                result += AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False).rule

                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X), pw.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == rcc5["disjoint"]:

                result = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False).rule
                result += AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), in(" + name2 + ",X).\n"
            elif self.relations == rcc5["overlaps"]:

                result = AggregationRule(firstVar=name1, secondVar=name2).rule
                result += AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == (rcc5["equals"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    ## TODO
                    result = ""
            elif self.relations == (rcc5["equals"] | rcc5["is_included_in"]):
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- in(" + name1 + ",X), out3(" + name2 + ", X, R), ix.\n"
                result += AggregationRule(firstVar=name1, secondVar=name2).rule
                result += "vr(X, r" + self.ruleNum.__str__() + ") " + disjointSymbol + " ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == (rcc5["equals"] | rcc5["includes"]):
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                result += "ir(X, prod(r" + self.ruleNum.__str__() + ",R)) :- out3(" + name1 + ", X, R), in(" + name2 + ",X), ix.\n"

                result += "vr(X, r" + self.ruleNum.__str__() + ") " + disjointSymbol + " ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                result += AggregationRule(firstVar=name1, secondVar=name2).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == (rcc5["is_included_in"] | rcc5["includes"]):
                result  = "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X), vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y).\n"

                aggrExpression = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False, addPW=False, lowerBound="0 < ", isConstraint=False).rule
                result += "ir(Y, r" + self.ruleNum.__str__() + ") :- " + aggrExpression + ", in(" + name2 + ",Y), out(" + name1 + ",Y).\n"

            elif self.relations == (rcc5["disjoint"] | rcc5["overlaps"]):

                result = "ir(X, r" + self.ruleNum.__str__() + ") " + disjointSymbol + " (X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), in(" + name2 + ",X).\n"
                result += AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False).rule

            elif self.relations == (rcc5["equals"] | rcc5["overlaps"]):
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False, lowerBound="0 < ", isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name2, secondVar=name1, secondPredIsIn=False, isConstraint=False, variableName="Y").rule
                result = twoPredFormat.format(firstRule, secondRule)
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False, isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name2, secondVar=name1, secondPredIsIn=False, lowerBound="0 < ", isConstraint=False, addPW=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)
                result += AggregationRule(firstVar=name1, secondVar=name2).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name2 + ", X), out(" + name1 + ", X), #count{Y: vr(Y, _), in(" + name1 + ",Y), out(" + name2 + ",Y)} > 0, ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), #count{Y: vr(Y, _), in(" + name2 + ",Y), out(" + name1 + ",Y)} > 0, ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"

            elif self.relations == (rcc5["is_included_in"] | rcc5["overlaps"]):

                result = "vr(X, r" + self.ruleNum.__str__() + ") " + disjointSymbol + " ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"

                result += AggregationRule(firstVar=name1, secondVar=name2).rule
                result += AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False).rule

            elif self.relations == (rcc5["is_included_in"] | rcc5["disjoint"]):
                result = AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False).rule
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, lowerBound="0 < ", isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name2, secondVar=name1, firstPredIsIn=False, lowerBound="0 < ", isConstraint=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name2, secondVar=name1, firstPredIsIn=False, isConstraint=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)

            elif self.relations == (rcc5["includes"] | rcc5["overlaps"]):
                result += "vrs(X) " + disjointSymbol + " irs(X) :- out(" + name1 + ",X), in(" + name2 + ",X), pw.\n"
                result += AggregationRule(firstVar=name1, secondVar=name2).rule
                result += AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False).rule


            elif self.relations == (rcc5["includes"] | rcc5["disjoint"]):

                result += AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False).rule
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, lowerBound="0 < ", isConstraint=False,
                                            addPW=False).rule
                secondRule = AggregationRule(firstVar=name2, secondVar=name1, secondPredIsIn=False, lowerBound="0 < ",
                                             isConstraint=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name2, secondVar=name1, secondPredIsIn=False,
                                             isConstraint=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), in(" + name1 + ", X), out(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", prod(A, B), 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), vr(Y, B), in("+ name2 + ",Y), out(" + name1 + ",Y), ix.\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["equals"]):

                result += "vr(X, r" + self.ruleNum.__str__() + ") " + disjointSymbol + " ir(X, r" + self.ruleNum.__str__() + ") :- out(" + name1 + ",X), in(" + name2 + ",X).\n"
                result += "vr(X, r" + self.ruleNum.__str__() + ") " + disjointSymbol + " ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False, lowerBound="0 < ", isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False, lowerBound="0 < ", isConstraint=False, addPW=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)
                result += AggregationRule(firstVar=name1, secondVar=name2).rule + "\n"

            elif self.relations == (rcc5["is_included_in"] | rcc5["equals"] | rcc5["overlaps"]):
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False, lowerBound="0 < ",
                                            isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False,
                                             isConstraint=False, addPW=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)
                result += AggregationRule(firstVar=name1, secondVar=name2).rule + "\n"

            elif self.relations == (rcc5["includes"] | rcc5["equals"] | rcc5["overlaps"]):
                firstRule = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False,
                                            isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False, lowerBound="0 < ",
                                             isConstraint=False, addPW=False, variableName="Y").rule
                result += twoPredFormat.format(firstRule, secondRule)
                result += AggregationRule(firstVar=name1, secondVar=name2).rule + "\n"

            elif self.relations == (rcc5["equals"] | rcc5["includes"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2 + ", X)} = 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} > 0.\n"
                    result += ":- #count{X: vrs(X), out(" + name1 + ", X), in(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 +", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), in(" + name1 + ", Z), out(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["equals"] | rcc5["is_included_in"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y:vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y:vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0.\n"
                    result += ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y:vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} = 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"]):

                firstRule = AggregationRule(firstVar=name1, secondVar=name2, secondPredIsIn=False,
                                            isConstraint=False, addPW=False).rule
                secondRule = AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False,
                                             isConstraint=False, addPW=False, variableName="Y").rule
                thirdRule = AggregationRule(firstVar=name1, secondVar=name2, lowerBound="0 < ",
                                            isConstraint=False, addPW=False, variableName="Z").rule
                result += threePredFormat.format(firstRule, secondRule, thirdRule)
                result += AggregationRule(firstVar=name1, secondVar=name2).rule + "\n"

            elif self.relations == (rcc5["disjoint"] | rcc5["equals"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result  = ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y : vrs(Y), out(" + name1 + ", Y ), in(" + name2 + ", Y )} = 0.\n"
                    result += ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y), out(" + name1 + ", Y ), in(" + name2 + ", Y )} > 0.\n"
                    result += ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y), in(" + name1 + ", Y ), in(" + name2 + ", Y )} = 0, #count{Z : vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["disjoint"] | rcc5["is_included_in"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"\
                           ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0, #count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["disjoint"] | rcc5["overlaps"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y ), out(" + name1 + ", Y), in(" + name2 + ", Y )} = 0.\n"\
                           ":- #count{X : vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y : vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y )} > 0, #count{Z : vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0, #count{Y: vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"\
                           ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0, #count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0, #count{Z : vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} = 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["disjoint"] | rcc5["is_included_in"] | rcc5["overlaps"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} = 0.\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["disjoint"] | rcc5["overlaps"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["disjoint"] | rcc5["equals"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} > 0,"\
                                "#count{Y: vrs(Y), in(" + name1 + ", Y), in(" + name2 + ", Y)} > 0,"\
                                "#count{Z: vrs(Z), out(" + name1 + ", Z), in(" + name2 + ", Z)} > 0.\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"] | rcc5["disjoint"]):
                if reasoner[rnr] == reasoner["dlv"]:
                    result = ":- #count{X: vrs(X), in(" + name1 + ", X), out(" + name2 + ", X)} = 0,"\
                                "#count{Y: vrs(Y), out(" + name1 + ", Y), in(" + name2 + ", Y)} = 0.\n"
                elif reasoner[rnr] == reasoner["clingo"]:
                    # TODO
                    result = ""
            elif self.relations == (rcc5["equals"] | rcc5["includes"] | rcc5["is_included_in"] | rcc5["overlaps"] | rcc5["disjoint"]):
                result = ""
            elif self.relations == relation["+="]: # lsum
                name3 = self.taxon3.dlvName()
                result = AggregationRule(firstVar=name1, secondVar=name3, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name1, secondVar=name3).rule
                result += AggregationRule(firstVar=name2, secondVar=name3, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name2, secondVar=name3).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), out(" + name2 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out(" + name2 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 4) :- ir(X, A), in(" + name2 + ", X), in(" + name3 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 4) :- vr(X, A), in(" + name2 + ", X), in(" + name3 + ", X), ix.\n\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name3 + ",X), pw.\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name3 + ",X), pw.\n"
            elif self.relations == relation["=-"]: # rdiff
                name3 = self.taxon3.dlvName()
                result = AggregationRule(firstVar=name1, secondVar=name2, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name1, secondVar=name2).rule
                result += AggregationRule(firstVar=name3, secondVar=name2, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name3, secondVar=name2).rule

                result += "pie(r" + self.ruleNum.__str__() + ", A, 1) :- ir(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 1) :- vr(X, A), out(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 2) :- ir(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 2) :- vr(X, A), in(" + name1 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 3) :- ir(X, A), out(" + name3 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 3) :- vr(X, A), out(" + name3 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "pie(r" + self.ruleNum.__str__() + ", A, 4) :- ir(X, A), in(" + name3 + ", X), in(" + name2 + ", X), ix.\n"
                result += "c(r" + self.ruleNum.__str__() + ", A, 4) :- vr(X, A), in(" + name3 + ", X), in(" + name2 + ", X), ix.\n\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name2 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name2 + ",X).\n"
            elif self.relations == relation["+3="]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                result = AggregationRule(firstVar=name1, secondVar=name4, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name1, secondVar=name4).rule
                result += AggregationRule(firstVar=name2, secondVar=name4, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name2, secondVar=name4).rule
                result += AggregationRule(firstVar=name3, secondVar=name4, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name3, secondVar=name4).rule

                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name4 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name4 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name4 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- out(" +name1 + ",X), out(" + name2 + ",X),\
                            out(" + name3 + ",X), in(" + name4 + ",X).\n"
            elif self.relations == relation["+4="]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                name5 = self.taxon5.dlvName()
                result = AggregationRule(firstVar=name1, secondVar=name5, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name1, secondVar=name5).rule
                result += AggregationRule(firstVar=name2, secondVar=name5, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name2, secondVar=name5).rule
                result += AggregationRule(firstVar=name3, secondVar=name5, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name3, secondVar=name5).rule
                result += AggregationRule(firstVar=name4, secondVar=name5, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name4, secondVar=name5).rule

                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name1 + ",X), out(" + name5 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name5 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name5 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out(" + name5 + ",X).\n"
            elif self.relations == relation["=+"] or self.relations == relation["-="]: # rsum and ldiff
                name3 = self.taxon3.dlvName()
                result = AggregationRule(firstVar=name2, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name2, secondVar=name1).rule
                result += AggregationRule(firstVar=name3, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name3, secondVar=name1).rule

                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name1 + ",X).\n"
            elif self.relations == relation["=3+"]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                result = AggregationRule(firstVar=name2, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name2, secondVar=name1).rule
                result += AggregationRule(firstVar=name3, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name3, secondVar=name1).rule
                result += AggregationRule(firstVar=name4, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name4, secondVar=name1).rule

                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out(" + name1 + ",X).\n"
            elif self.relations == relation["=4+"]:
                name3 = self.taxon3.dlvName()
                name4 = self.taxon4.dlvName()
                name5 = self.taxon5.dlvName()
                result = AggregationRule(firstVar=name2, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name2, secondVar=name1).rule
                result += AggregationRule(firstVar=name3, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name3, secondVar=name1).rule
                result = AggregationRule(firstVar=name4, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name4, secondVar=name1).rule
                result += AggregationRule(firstVar=name5, secondVar=name1, firstPredIsIn=False).rule
                result += AggregationRule(firstVar=name5, secondVar=name1).rule

                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name2 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name3 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name4 + ",X), out(" + name1 + ",X).\n"
                result += "ir(X, r" + self.ruleNum.__str__() + ") :- in(" + name5 + ",X), out(" + name1 + ",X).\n"
            else:
                print("Relation ",self.relations," is not yet supported!!!!")
                result = "\n"
        elif encode[enc] & encode["direct"]:
            prefix = "label(" + name1 + ", " + name2 +", "
            result = ""
            firstrel = True
            if self.relations < relation["+="]:
                if self.relations & rcc5["includes"] == rcc5["includes"]:
                    result  = prefix + "in) "
                    firstrel = False
                if self.relations & rcc5["is_included_in"] == rcc5["is_included_in"]:
                    if firstrel:
                        result  = prefix + "ls) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "ls) "
                if self.relations & rcc5["overlaps"] == rcc5["overlaps"]:
                    if firstrel:
                        result  = prefix + "ol) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "ol) "
                if self.relations & rcc5["disjoint"] == rcc5["disjoint"]:
                    if firstrel:
                        result  = prefix + "ds) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "ds) "
                if self.relations & rcc5["equals"] == rcc5["equals"]:
                    if firstrel:
                        result  = prefix + "eq) "
                        firstrel = False
                    else:
                        result += " v " + prefix + "eq) "
                if not firstrel:
                    result += "."
            elif self.relations == relation["+="]:
                result = "sum(" + self.taxon3.dlvName() + "," + name1 + "," + name2 + ").\n"
            elif self.relations == relation["=+"]:
                result = "sum(" + name1 + "," + name2 + "," + self.taxon3.dlvName() + ").\n"
        else:
            raise Exception("Encoding:", enc, " is not supported !!")
        return result
