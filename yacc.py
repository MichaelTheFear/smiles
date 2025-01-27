from sly import Parser
from lex import SmilesLex
import chem

class SmilesParser(Parser):
    # Use tokens from the lexer
    tokens = SmilesLex.tokens

    @_('atom', 'atom chain_branch') # type: ignore
    def line(self, rules):
        pass
    
    @_('chains', 'branch', 'chains chain_branch', 'branch chain_branch')  # type: ignore
    def chain_branch(self,rules):
        pass
    
    @_('chain', 'chain chains')  # type: ignore
    def chains(self, rules):
        pass
    
    @_('"[" opt_isotope symbol opt_chiral opt_hcount opt_charge opt_map "]"')  # type: ignore
    def bracket_atom(self,rules):
        chem.validate_valency_mol(rules.opt_isotope, rules.symbol,
                                  rules.opt_chiral, rules.opt_hcount,
                                  rules.opt_charge, rules.opt_map)
        
        pass
    
    @_('"." atom', 'opt_bond atom', 'opt_bond rnum')  # type: ignore
    def chain(self,rules):
        pass
    
    @_('semi_symbol', 'organic_symbol')  # type: ignore
    def symbol(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('"(" inner_branch ")"')  # type: ignore
    def branch(self,rules):
        pass
    
    @_('opt_bond_dot line', 'opt_bond_dot line inner_branch')  # type: ignore
    def inner_branch(self,rules):
        pass
    
    @_('bond','')  # type: ignore
    def opt_bond(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('isotope','')  # type: ignore
    def opt_isotope(self,rules):
        return rules[0] if len(rules) > 0 else None

    @_('chiral','')  # type: ignore
    def opt_chiral(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('hcount','')  # type: ignore
    def opt_hcount(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('bond','"."','')  # type: ignore
    def opt_bond_dot(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('charge','')  # type: ignore
    def opt_charge(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('map','')  # type: ignore
    def opt_map(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('digit','')  # type: ignore
    def opt_digit(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('semi_bond', '"-"')  # type: ignore
    def bond(self,rules):
        return rules[0] if len(rules) > 0 else None
    
    @_('"H"', 'semi_organic_symbol')  # type: ignore
    def organic_symbol(self,rules):
        pass
    
    @_('organic_symbol', 'bracket_atom')  # type: ignore
    def atom(self,rules):
        pass
    
    @_('digit', '"%" digit digit ')  # type: ignore
    def rnum(self,rules):
        pass
    
    @_('opt_digit opt_digit digit')  # type: ignore
    def isotope(self,rules):
        pass
    
    @_('"H" opt_digit')  # type: ignore
    def hcount(self,rules):
        pass
    
    @_('"+"', '"+" "+"', '"-"', '"-" "-"', '"-" fifteen', '"+" fifteen')  # type: ignore
    def charge(self,rules):
        pass
    
    @_('":" opt_digit opt_digit digit')  # type: ignore
    def map(self,rules):
        pass
    
    @_('"@"', '"@" "@"')  # type: ignore
    def chiral(self,rules):
        pass
    
    @_('digit digit', 'digit')  # type: ignore
    def fifteen(self,rules):
        pass

# Instantiate and use the parser
parser = SmilesParser()
lexer = SmilesLex()
result = parser.parse(lexer.tokenize("[AuH2]"))

