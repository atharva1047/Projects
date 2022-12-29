import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])
            
            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_rule):
        """Retract a fact or a rule from the KB

        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_rule])
        ####################################################
        # Student code goes here

        
        # for rule
        if isinstance(fact_rule, Rule):
            fact_rule = self._get_rule(fact_rule)
        elif isinstance(fact_rule, Fact):
            fact_rule = self._get_fact(fact_rule)
        
        if fact_rule.asserted:
            fact_rule.asserted = False
        
        if len(fact_rule.supported_by) != 0:
            return None

        if isinstance(fact_rule, Rule):
            self.rules.remove(fact_rule)
        if isinstance(fact_rule, Fact):
            self.facts.remove(fact_rule)
        

        # removing inferred or supported facts
        for fact in fact_rule.supports_facts:
            fact = self._get_fact(fact)
            fact_len = 0
            total_len = len(fact.supported_by)

            for parent_facts in fact.supported_by:
                if fact_rule in parent_facts:
                    fact.supported_by.remove(parent_facts)
                    fact_len += 1
            if (total_len == fact_len) and (fact.asserted == False):
                self.kb_retract(fact)
        
        # removing inferred or supported rules
        for rule in fact_rule.supports_rules:
            rule = self._get_rule(rule)
            rule_len = 0
            total_len = len(rule.supported_by)
            for parent_rules in rule.supported_by:
                if fact_rule in parent_rules:
                    rule.supported_by.remove(parent_rules)
                    rule_len += 1
            if (total_len == rule_len) and (rule.asserted == False):
                self.kb_retract(rule)


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        #print(f'Fact: {fact} and Rule: {rule}')
        #print(f'Attempting to infer from {fact.statement} and {rule.lhs[0]} => {rule.rhs}')
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        # Student code goes here

        possible_bindings = match(fact.statement, rule.lhs[0])
        rule_statements_lhs = []
       
        if possible_bindings != False:
            bind_to_rhs = instantiate(rule.rhs, possible_bindings)
 
            if len(rule.lhs) > 1:
                for i in rule.lhs[1:]:
                    bind_to_lhs = instantiate(i, possible_bindings)
                    rule_statements_lhs.append(bind_to_lhs)
               
                new_rule = Rule([rule_statements_lhs, bind_to_rhs], [[fact, rule]])
                rule.supports_rules.append(new_rule)
                fact.supports_rules.append(new_rule)
                kb.kb_assert(new_rule)
               
                return None
           
 
            new_fact = Fact(bind_to_rhs, [[fact, rule]])
            rule.supports_facts.append(new_fact)
            fact.supports_facts.append(new_fact)
            kb.kb_assert(new_fact)
 
            return None


