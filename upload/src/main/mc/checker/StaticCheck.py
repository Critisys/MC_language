
"""
 * @author nhphung
"""
# 1711700

from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce 

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value



class StaticChecker(BaseVisitor,Utils):

    global_envi = [
    Symbol("getInt",MType([],IntType())),
    Symbol("putInt",MType([IntType()],VoidType())),
    Symbol("putIntLn",MType([IntType()],VoidType())),
    Symbol("getFloat",MType([],FloatType())),
    Symbol("putFloat",MType([FloatType()],VoidType())),
    Symbol("putFloatLn",MType([FloatType()],VoidType())),
    Symbol("putBool",MType([BoolType()],VoidType())),
    Symbol("putBoolLn",MType([BoolType()],VoidType())),
    Symbol("putString",MType([StringType()],VoidType())),
    Symbol("putStringLn",MType([StringType()],VoidType())),
    Symbol("putLn",MType([],VoidType()))
    ]
            
    
    def __init__(self,ast):
        #print(ast)
        #print(ast)
        #print()
        self.ast = ast

    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def Lookup_decl(self,name,list_decl):
        for x in list_decl:
            if type(x) is Symbol:
                if name == x.name:
                    return x
            elif type(x) is list:
                return self.Lookup_decl(self,x)
        return None 

    def checkRedeclare(self,kind,name,list_decl):
        x = self.Lookup_decl(name,list_decl)
        if x is not None:
            raise Redeclared(kind, name)
        return False

    def addReference(self,ref_env,decl):
        x = self.Lookup_decl(decl.name,ref_env)
        if x is not None:
            ref_env.remove(x)
            ref_env.append(decl)
        else:
            ref_env.append(decl)
        return True

    def visitProgram(self,ast, c): 
        decl_global = c[:]
        func_to_invoke = []
        for d in ast.decl:
            if type(d) is VarDecl:
                self.checkRedeclare(Variable(),d.variable,decl_global)
                decl_global.append(Symbol(d.variable,d.varType))
            elif type(d) is FuncDecl:
                self.checkRedeclare(Function(),d.name.name,decl_global)
                decl_global.append(Symbol(d.name.name,MType([i.varType for i in d.param],d.returnType)))
                func_to_invoke.append(d.name.name)

        if "main" not in func_to_invoke:
            raise NoEntryPoint()

        func_to_invoke.remove("main")
        allcheck = []
        for i in ast.decl:
            check = []
            if type(i) is FuncDecl:
                self.visit(i,[decl_global,check])
                if i.name.name in check:
                    check.remove(i.name.name)
            allcheck = allcheck + check
        
        for i in func_to_invoke:
            if i not in allcheck:
                raise UnreachableFunction(i)

        return True

    def visitVarDecl(self,ast, c):
        self.checkRedeclare(Variable(),ast.variable,c)
        return Symbol(ast.variable,ast.varType)
        

    def visitFuncDecl(self,ast, c): 
        decl_local= []
        ref_env = c[0][:]
        for x in ast.param:
            if self.Lookup_decl(x.variable,decl_local) is not None:
                raise Redeclared(Parameter(),x.variable)
            else:
                decl_local.append(Symbol(x.variable,x.varType))
                self.addReference(ref_env,Symbol(x.variable,x.varType))

        local_stmt = []
        for x in ast.body.member:
            if type(x) is VarDecl:
                decl_local.append(self.visit(x,decl_local))
                self.addReference(ref_env,Symbol(x.variable,x.varType))
            elif isinstance(x,Expr):
                self.visit(x,[ref_env,c[1]])
            else:
                local_stmt.append(self.visit(x,[ref_env,ast.returnType,False,c[1]]))

        if type(ast.returnType) is not VoidType:
            if True not in local_stmt:
                raise FunctionNotReturn(ast.name.name)

    def visitId(self,ast,c):
        x = self.Lookup_decl(ast.name,c[0])
        if x is None:
            raise Undeclared(Identifier(),ast.name)
        
        return x.mtype
        
    def visitCallExpr(self,ast,c):
        x = self.Lookup_decl(ast.method.name,c[0])
        if x is None:
            raise Undeclared(Function(),ast.method.name)
        elif type(x.mtype) is not MType:
            raise TypeMismatchInExpression(ast)
        elif len(ast.param) != len(x.mtype.partype):
            raise TypeMismatchInExpression(ast)
        
        idx = 0
        for para in ast.param:
            if type(x.mtype.partype[idx]) is IntType and type(self.visit(para,c)) is IntType:
                idx += 1
            elif type(x.mtype.partype[idx]) is FloatType and type(self.visit(para,c)) in [IntType,FloatType]:
                idx += 1
            elif type(x.mtype.partype[idx]) is StringType and type(self.visit(para,c)) is StringType:
                idx += 1
            elif type(x.mtype.partype[idx]) is BoolType and type(self.visit(para,c)) is BoolType:
                idx += 1
            elif type(x.mtype.partype[idx]) is ArrayPointerType and type(self.visit(para,c)) in [ArrayType,ArrayPointerType]:
                if type(x.mtype.partype[idx].eleType) is type(self.visit(para,c).eleType):
                    idx += 1
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise TypeMismatchInExpression(ast)
        
        if ast.method.name not in c[1]:
            c[1].append(ast.method.name)
        return x.mtype.rettype 

    def visitIntLiteral(self, ast, c):
        return IntType()

    def visitFloatLiteral(self, ast, c):
        return FloatType()

    def visitBooleanLiteral(self, ast, c):
        return BoolType()

    def visitStringLiteral(self, ast, c):
        return StringType()

    def visitArrayCell(self,ast,c):
        if type(self.visit(ast.arr,c)) in [ArrayType,ArrayPointerType]:
            if type(self.visit(ast.idx,c)) is IntType:
                return self.Lookup_decl(ast.arr.name,c[0]).mtype.eleType
        raise TypeMismatchInExpression(ast)

    def visitUnaryOp(self,ast,c):
        ret = self.visit(ast.body,c)
        if ast.op == "-":
            if type(ret) in [IntType,FloatType]:
                return ret
            else:
                raise TypeMismatchInExpression(ast)
        else:
            if type(ret) is BoolType:
                return ret
            else:
                raise TypeMismatchInExpression(ast)

    def visitBinaryOp(self,ast,c):
        lh = self.visit(ast.left,c)
        rh = self.visit(ast.right,c)
        if ast.op == "=":
            if type(ast.left) in [Id,ArrayCell]:
                if type(lh) is IntType and type(rh) is IntType:
                    return IntType()
                elif type(lh) is FloatType and type(rh) in [IntType,FloatType]:
                    return FloatType()
                elif type(lh) is StringType and type(rh) is StringType:
                    return StringType()
                elif type(lh) is BoolType and type(rh) is BoolType:
                    return BoolType()
                else:
                    raise TypeMismatchInExpression(ast)
            else:
                raise NotLeftValue(ast.left)
        elif ast.op in ["+","-","*","/"]:
            if type(lh) is IntType and type(rh) is IntType:
                return IntType()
            elif type(lh) in [IntType,FloatType] and type(rh) in [IntType,FloatType]:
                return FloatType()
            else:
                raise TypeMismatchInExpression(ast)
        elif ast.op == "%":
            if type(lh) is IntType and type(rh) is IntType:
                return IntType()
            else:
                raise TypeMismatchInExpression(ast)
        elif ast.op in [">",">=","<",'<=']:
            if type(lh) in [IntType,FloatType] and type(rh) in [IntType,FloatType]:
                return BoolType()
            else:
                raise TypeMismatchInExpression(ast)
        elif ast.op in ["==","!="]:
            if type(lh) in [IntType,FloatType,StringType,BoolType] and type(rh) is type(lh):
                return BoolType()
            else:
                raise TypeMismatchInExpression(ast)

    def visitIf(self,ast,c):
        if type(self.visit(ast.expr,[c[0],c[3]])) is not BoolType:
            raise TypeMismatchInStatement(ast)
        if isinstance(ast.thenStmt,Expr):
            self.visit(ast.expr,[c[0],c[3]])
            ret = []
        else:
            ret = [self.visit(ast.thenStmt,c)]


        if ast.elseStmt:
            if isinstance(ast.elseStmt,Expr):
                self.visit(ast.elseStmt,[c[0],c[3]])
                ret.append(False)
            else:
                ret.append(self.visit(ast.elseStmt,c))
            
        if False in ret:
            return False
        else:
            return True

    def visitFor(self,ast,c):
        if type(self.visit(ast.expr1,[c[0],c[3]])) is not IntType:
            raise TypeMismatchInStatement(ast)
        elif type(self.visit(ast.expr2,[c[0],c[3]])) is not BoolType:
            raise TypeMismatchInStatement(ast)
        elif type(self.visit(ast.expr3,[c[0],c[3]])) is not IntType:
            raise TypeMismatchInStatement(ast)
        
        if isinstance(ast.loop,Expr):
            self.visit(ast.loop,[c[0],c[3]])
        else:
            ret = [self.visit(ast.loop,[c[0],c[1],True,c[3]])]
        
        return False

    def visitDowhile(self,ast,c):
        if type(self.visit(ast.exp,[c[0],c[3]])) is not BoolType:
            raise TypeMismatchInStatement(ast)

        ret = []
        for x in ast.sl:
            if isinstance(x,Expr):
                self.visit(x,[c[0],c[3]])
            else:
                ret.append(self.visit(x,[c[0],c[1],True,c[3]]))
        if True in  ret:
            return True
        else:
            return False

    def visitBreak(self,ast,c):
        if c[2] == True:
            return False
        else:
            raise BreakNotInLoop()
    
    def visitContinue(self,ast,c):
        if c[2] == True:
            return False
        else: 
            raise ContinueNotInLoop()

    def visitReturn(self,ast,c):
        if ast.expr:
            if type(self.visit(ast.expr,[c[0],c[3]])) in [ArrayPointerType,ArrayType] and type(c[1]) is ArrayPointerType:
                if type(self.visit(ast.expr,[c[0],c[3]]).eleType) is type(c[1].eleType):
                    return True
                else:
                    raise TypeMismatchInStatement(ast)
            elif type(self.visit(ast.expr,[c[0],c[3]])) in [FloatType,IntType] and type(c[1]) is FloatType:
                return True
            elif type(self.visit(ast.expr,[c[0],c[3]])) is IntType and type(c[1]) is IntType:
                return True
            elif type(self.visit(ast.expr,[c[0],c[3]])) is type(c[1]):
                return True
            else: 
                raise TypeMismatchInStatement(ast)
        elif type(c[1]) is VoidType:
            return True
        else:
            raise TypeMismatchInStatement(ast)
        
    def visitBlock(self,ast,c):
        decl_local= []
        ref_env = c[0][:]

        local_stmt = []
        for x in ast.member:
            if type(x) is VarDecl:
                decl_local.append(self.visit(x,decl_local))
                self.addReference(ref_env,Symbol(x.variable,x.varType))
            elif isinstance(x,Expr):
                self.visit(x,[ref_env,c[3]])
            else:
                local_stmt.append(self.visit(x,[ref_env,c[1],c[2],c[3]]))
        if True in local_stmt:
            return True
        else:
            return False