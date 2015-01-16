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

from utility import *
import re
import pdb

class LatentTaxAssumption:
    name = ""
    
    def toLTax(self, taxonomies):
        return null

    def getLTAFromAbbrev(self, abbrev):
        abbrev = abbrev.upper()
        if (abbrev == "N"):
            return NonEmptiness()
        elif (abbrev == "D"):
            return DisjointChildren()
        elif (abbrev == "C"):
            return Coverage()
    
    def getLTAsFromString(self, ltaString):
        result = []
        elements = ltaString.split(",")
        
        for element in elements:
            subResult = []
            if (not(element == "none")):
                for lta in element:
                    subResult.append(self.getLTAFromAbbrev(lta))   
            result.append(subResult)
        return result
    

    ## returns a list of lists
    ## each list contains the LTAs to be applied
    ## the LTAs are actual instances of their respective classes
    ## clever - perhaps too clever!
    ## in fact, I don't think it's called anymore
    #def powerSet(self, ltas=["NonEmptiness()","DisjointChildren()","Coverage()"]):
    #  result = []
    #  numCombinations = pow(2,len(ltas))
    # for loop in range(0, numCombinations):
    #      newList = []
    #      binary = paddedBase10toN(loop,2,len(ltas))
    #      for inloop in range(0,len(binary)):
    #          if (binary[inloop] == "1"):
    #              newList += [eval(ltas[inloop])]          
    #      result.append(newList)          
    #  return result        
          
            
class NonEmptiness(LatentTaxAssumption):
    name = "NonEmptiness"
    abbrev = "N"
    
    def __str__(self):
        return self.abbrev
    
    def toLTax(self, taxonomies):
        result = ""
        doneList = []
        for taxonomy in taxonomies.taxonomies.values():
            for taxon in taxonomy.taxa.values():
                name = taxon.stringOfReasoner()
                if ((name in doneList) == False):
                    doneList.append(name)
                    result += "exists x " + name + "(x).\n"   
        return result
    
class DisjointChildren(LatentTaxAssumption):
    name = "DisjointChildren"
    abbrev = "D"

    def __str__(self):
        return self.abbrev
        
    def toLTax(self, taxonomies):
        result = ""
        for taxonomy in taxonomies.taxonomies.values():
            for taxon in taxonomy.taxa.values():
                if (taxon.hasChildren()):
                    for child in taxon.children:
                        for child2 in taxon.children:
                            if (child.stringOf() > child2.stringOf()):
                                result += "(all x (" + child.stringOfReasoner() + "(x) -> -" + child2.stringOfReasoner() + "(x))).\n"
                ### deal with multiple top level nodes
		for taxon2 in taxonomy.taxa.values():                   
			if ((taxon in taxonomy.roots) and (taxon2 in taxonomy.roots) and (taxon.stringOf() > taxon2.stringOf())):
                                result += "(all x (" + taxon.stringOfReasoner() + "(x) -> -" + taxon2.stringOfReasoner() + "(x))).\n"
                                result += "(all x (" + taxon2.stringOfReasoner() + "(x) -> -" + taxon.stringOfReasoner() + "(x))).\n"
                                #result += taxon.stringOf() + " " + taxon2.stringOf() + " ( DC )\n"


        return result

    
class Coverage(LatentTaxAssumption):
    name = "Coverage"
    abbrev = "C"

    def __str__(self):
        return self.abbrev
    
    def toLTax(self, taxonomies):
        result = ""
        for taxonomy in taxonomies.taxonomies.values():
            for taxon in taxonomy.taxa.values():
                if (taxon.hasChildren()):
                    result += taxon.stringOfReasoner() + "(x) -> "
                    for child in taxon.children:
                        if (child != taxon.children[0]):
                            result += " | "
                        result += child.stringOfReasoner() + "(x)"
                    result += ".\n"
        return result
