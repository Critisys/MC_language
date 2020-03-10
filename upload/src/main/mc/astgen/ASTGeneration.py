# 1711700
from MCVisitor import MCVisitor
from MCParser import MCParser
from AST import *
from functools import reduce

class ASTGeneration(MCVisitor):
    def visitProgram (self, ctx:MCParser.ProgramContext):
        return Program(list(reduce(lambda x,y: x + self.visit(y),ctx.decl(),[])))
    
    def visitDecl(self, ctx:MCParser.DeclContext):
        return self.visit(ctx.var_decl()) if ctx.var_decl() else self.visit(ctx.func_decl())

    def visitVar_decl(self, ctx: MCParser.Var_declContext):
        lst = []
        for x in ctx.one_id():
            if x.getChildCount() == 1:
                lst.append(VarDecl(x.ID().getText(), self.visit(ctx.prim_type())))
            else:
                lst.append(VarDecl(x.ID().getText(),ArrayType(int(x.INTLIT().getText()),self.visit(ctx.prim_type()))))

        return lst 

    def visitPrim_type(self, ctx: MCParser.Prim_typeContext):
        if ctx.INTTYPE():
            return IntType()
        elif ctx.FLOATTYPE():
            return FloatType()
        elif ctx.BOOLTYPE():
            return BoolType()
        elif ctx.STRINGTYPE():
            return StringType()

    def visitFunc_decl(self, ctx: MCParser.Func_declContext):
        return [FuncDecl(Id(ctx.ID().getText()),self.visit(ctx.para_list()),self.visit(ctx.all_type()),self.visit(ctx.block_stmt()))]

    def visitAll_type(self, ctx: MCParser.All_typeContext):
        if ctx.getChildCount() == 3:
            return ArrayPointerType(self.visit(ctx.prim_type()))
        elif ctx.prim_type():
            return self.visit(ctx.prim_type())
        elif ctx.VOIDTYPE():
            return VoidType()

    def visitPara_list(self, ctx: MCParser.Para_listContext):
        return [self.visit(x) for x in ctx.para()] if ctx.para() else []

    def visitPara(self, ctx: MCParser.ParaContext):
        return VarDecl(ctx.ID().getText(),ArrayPointerType(self.visit(ctx.prim_type()))) if ctx.getChildCount() == 4 else VarDecl(ctx.ID().getText(),self.visit(ctx.prim_type()))

    def visitBlock_stmt(self, ctx: MCParser.Block_stmtContext):
        return Block(list(reduce(lambda x,y: x + self.visit(y),ctx.body(),[])))

    def visitBody(self, ctx: MCParser.BodyContext):
        return self.visit(ctx.var_decl()) if ctx.var_decl() else [self.visit(ctx.stmt())]

    def visitStmt(self, ctx: MCParser.StmtContext):
        return self.visit(ctx.getChild(0))

    def visitIf_stmt(self, ctx: MCParser.If_stmtContext):
        return self.visit(ctx.getChild(0))

    def visitMatch_if(self, ctx: MCParser.Match_ifContext):
        return If(self.visit(ctx.exp()),self.visit(ctx.other_stmt()),self.visit(ctx.stmt())) if ctx.other_stmt() else If(self.visit(ctx.exp()),self.visit(ctx.match_if()),self.visit(ctx.stmt()))
    
    def visitOther_stmt(self, ctx: MCParser.Other_stmtContext):
        return self.visit(ctx.getChild(0))

    def visitUnmatch_if(self, ctx: MCParser.Unmatch_ifContext):
        return If(self.visit(ctx.exp()),self.visit(ctx.stmt()))
    
    def visitFor_stmt(self, ctx: MCParser.For_stmtContext):
        return For(self.visit(ctx.exp()[0]),self.visit(ctx.exp()[1]),self.visit(ctx.exp()[2]),self.visit(ctx.stmt()))
    
    def visitDowhile_stmt(self, ctx: MCParser.Dowhile_stmtContext):
        return Dowhile([self.visit(x) for x in ctx.stmt()],self.visit(ctx.exp()))

    def visitBreak_stmt(self, ctx: MCParser.Break_stmtContext):
        return Break()

    def visitContinue_stmt(self, ctx: MCParser.Continue_stmtContext):
        return Continue()

    def visitReturn_stmt(self, ctx: MCParser.Return_stmtContext):
        return Return(self.visit(ctx.exp())) if ctx.exp() else Return()
    
    def visitExp(self, ctx: MCParser.ExpContext):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.ASSIGN().getText(),self.visit(ctx.exp1()),self.visit(ctx.exp()))
        else:
            return self.visit(ctx.exp1())
    
    def visitExp1(self, ctx: MCParser.Exp1Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.OR().getText(),self.visit(ctx.exp1()),self.visit(ctx.exp2()))
        else:
            return self.visit(ctx.exp2())

    def visitExp2(self, ctx: MCParser.Exp2Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.AND().getText(),self.visit(ctx.exp2()),self.visit(ctx.exp3()))
        else:
            return self.visit(ctx.exp3())

    def visitExp3(self, ctx: MCParser.Exp3Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.exp4(0)),self.visit(ctx.exp4(1)))
        else:
            return self.visit(ctx.exp4(0))

    def visitExp4(self, ctx: MCParser.Exp4Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.exp5(0)),self.visit(ctx.exp5(1)))
        else:
            return self.visit(ctx.exp5(0))
    
    def visitExp5(self, ctx: MCParser.Exp5Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.exp5()),self.visit(ctx.exp6()))
        else:
            return self.visit(ctx.exp6())
   
    def visitExp6(self, ctx: MCParser.Exp6Context):
        if ctx.getChildCount() == 3:
            return BinaryOp(ctx.getChild(1).getText(),self.visit(ctx.exp6()),self.visit(ctx.exp7()))
        else:
            return self.visit(ctx.exp7())

    def visitExp7(self, ctx: MCParser.Exp7Context):
        if ctx.getChildCount() == 2:
            return UnaryOp(ctx.getChild(0).getText(), self.visit(ctx.exp7()))
        else:
            return self.visit(ctx.indexexp())
    
    def visitIndexexp(self, ctx: MCParser.IndexexpContext):
        if ctx.getChildCount() == 4:
            return ArrayCell(self.visit(ctx.exp8()),self.visit(ctx.exp()))
        else:
            return self.visit(ctx.exp8())

    def visitExp8(self, ctx: MCParser.Exp8Context):
        if ctx.getChildCount() == 3:
            return self.visit(ctx.exp())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.literal():
            return self.visit(ctx.literal())
        else: 
            return self.visit(ctx.funcall())

    def visitLiteral(self, ctx: MCParser.LiteralContext):
        if ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.BOOLLIT():
            return BooleanLiteral(bool("1")) if ctx.BOOLLIT().getText() == 'true' else BooleanLiteral(bool(""))
    
    def visitFuncall(self, ctx: MCParser.FuncallContext):
        return CallExpr(Id(ctx.ID().getText()),[self.visit(x) for x in ctx.exp()])