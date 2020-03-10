import unittest
from TestUtils import TestChecker
from AST import *

class CheckSuite(unittest.TestCase):

    # TEST FOR REDECLARED VARIABLE

    def test_redeclared_variable_a_global(self):
        input = """
                    int a;
                    int a;
                    void main(){
                    }
                    
                """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,400))

    def test_redeclared_variable_a_inside_function(self):
        input = """
                    void main(){
                        int a,a;
                    } 
                """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_redeclared_variable_with_different_type(self):
        input = """
                    void main(){
                        int a;
                        float a[5];
                    }
                    
                """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_redeclared_variable_with_exist_parameter(self):
        input = """
                    void main(int b){
                        string b;
                    }
                    
                """
        expect = "Redeclared Variable: b"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_redeclared_variable_in_same_scope(self):
        input = """
                    void main(){
                        int a,b;
                        {
                            float b;
                        }
                        string a;
                    }
                    
                """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_redeclared_variable_with_built_in_func(self):
        input = """ 
                    string putIntLn[5];
                    void main(int b){
                    }
                    
                """
        expect = "Redeclared Variable: putIntLn"
        self.assertTrue(TestChecker.test(input,expect,405))

    # TEST FOR REDECLARED PARAMETER

    def test_redeclared_parameter_a(self):
        input = """
                    int foo(int a, int a){
                        return 5;
                    }
                    void main(){
                    }
                    
                """
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_redeclared_parameter_b_with_type(self):
        input = """
                    void main(string b, int a, float b[]){
                        a + 1;
                    }
                    
                """
        expect = "Redeclared Parameter: b"
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_redeclared_parameter_a_with_type(self):
        input = """
                    void main(int ab, int a, int c, string a){
                    }
                    
                """
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,408))

    #  TEST FOR REDECLARED FUNCTION

    def test_redeclared_function_foo(self):
        input = """
                    int foo(){
                        return 2;
                    }
                    int foo(){
                        return 3;
                    }
                    void main(){
                    }
                    
                """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_redeclared_function_foo_with_different_type(self):
        input = """
                    int foo(){
                        return 2;
                    }
                    void main(){
                    }
                    string[] foo(){
                        string a[5];
                        return a;
                    }
                    
                """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_redeclared_function_foo_with_different_parameter(self):
        input = """
                    int foo(int a){
                        return 2;
                    }
                    void main(){
                        int a;
                        foo(a);
                    }
                    int foo(float b, int c){
                        return 5;
                    }
                    
                """
        expect = "Redeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,411))

    def test_redeclared_function_with_built_in_func(self):
        input = """
                    void main(){

                    }
                    int getFloat(){
                        float a;
                        a = 1;
                        return a;
                    }
                """
        expect = "Redeclared Function: getFloat"
        self.assertTrue(TestChecker.test(input,expect,412))

    # TEST FOR UNDECLARED IDENTIFIER

    def test_undeclared_variable_a(self):
        input = """
                    void main(){
                        a;
                    }
                    
                """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,413))

    def test_undeclared_variable_b_in_binary(self):
        input = """
                    int a;
                    void main(){
                        a = b;
                    }
                    
                """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,414))
    
    def test_undeclared_id_array(self):
        input = """
                    int a;
                    void main(){
                        a = 1;
                        b[a];
                    }
                    
                """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,415))

    def test_undeclared_variable_a_in_unary(self):
        input = """
                    void main(){
                        -a;
                    }
                    
                """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_undeclared_variable_b_in_call(self):
        input = """
                    int a(int b){
                        return 5;
                    }
                    void main(){
                        a(b);
                    }
                    
                """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_undeclared_variable_a_in_cell(self):
        input = """
                    void main(){
                        int b[5];
                        b[a];
                    }
                    
                """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_undeclared_variable_a_in_stmt(self):
        input = """ int b;
                    void main(){
                        b = 1;
                        do
                            a + 1;
                            b;
                        while(true);
                    }
                    
                """
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,419))

    # TEST FOR UNDECLARED FUNCTION

    def test_undeclared_function(self):
        input = """
                    void main(){
                        foo();
                    }
                    
                """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_undeclared_function_in_unary(self):
        input = """
                    void main(){
                        !foo();
                    }
                    
                """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,421))

    def test_undeclared_function_in_binary(self):
        input = """
                    void main(){
                        int a;
                        a = foo();
                    }
                    
                """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,422))

    def test_undeclared_function_in_stmt(self):
        input = """
                    void main(){
                        boolean a;
                        a = false;
                        if(foo(a)) return;
                    }
                    
                """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,423))

    def test_undeclared_function_in_funcall(self):
        input = """
                    int a(int b){
                        return 3;
                    }
                    void main(){
                        a(foo());
                    }
                    
                """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,424))

    def test_undeclared_function_in_arrcell(self):
        input = """
                    void main(){
                        string a[5];
                        string b;
                        b = a[foo()];
                    }
                    
                """
        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(input,expect,425))


    # TEST FOR TYPE MISMATCH IN IF STATEMENT

    def test_correct_if_stmt(self):
        input = """
                    void main(){
                        boolean a;
                        a = true;
                        if(a) return;
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,426))

    def test_if_stmt_mismatch_with_literal(self):
        input = """
                    void main(){
                        if(1) return;
                    }
                """
        expect = "Type Mismatch In Statement: If(IntLiteral(1),Return())"
        self.assertTrue(TestChecker.test(input,expect,427))

    def test_if_stmt_mismatch_with_id(self):
        input = """
                    void main(){
                        float a;
                        a = 2;
                        if(a) a + 1;
                    }
                """
        expect = "Type Mismatch In Statement: If(Id(a),BinaryOp(+,Id(a),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,428))
    
    def test_if_stmt_mismatch_with_exp(self):
        input = """
                    void main(){
                        int a;
                        a = 1;
                        if(a = 1 * -a) return;
                    }
                """
        expect = "Type Mismatch In Statement: If(BinaryOp(=,Id(a),BinaryOp(*,IntLiteral(1),UnaryOp(-,Id(a)))),Return())"
        self.assertTrue(TestChecker.test(input,expect,429))

    def test_if_stmt_mismatch_with_elsestmt(self):
        input = """
                    void main(){
                        float b;
                        b = 1;
                        if(b*1) b*2;
                        else b*1;
                    }
                """
        expect = "Type Mismatch In Statement: If(BinaryOp(*,Id(b),IntLiteral(1)),BinaryOp(*,Id(b),IntLiteral(2)),BinaryOp(*,Id(b),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,430))

    def test_if_stmt_mismatch_with_callexpr(self):
        input = """ 
                    string foo(int a){
                        return "A";
                    }
                    void main(){
                        string b;
                        if(foo(b)) b;
                        else return ;
                    }
                """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[Id(b)])"
        self.assertTrue(TestChecker.test(input,expect,431))

    # TEST FOR TYPE MISMATCH IN FOR STMT

    def test_correct_for_stmt(self):
        input = """
                    void main(){
                        int a,b[5];
                        b[5] = 1;
                        a = 1;
                        for(a = 1; a < 5; a = a + 1) b[5] = b[5] + a;
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,432))

    def test_for_stmt_mismatch_1st_exp(self):
        input = """
                    void main(){
                        float a;
                        int b;
                        b = 1;
                        a = 1;
                        for(a = 1; a < 5; 5) b = b + 1;
                    }
                """
        expect = "Type Mismatch In Statement: For(BinaryOp(=,Id(a),IntLiteral(1));BinaryOp(<,Id(a),IntLiteral(5));IntLiteral(5);BinaryOp(=,Id(b),BinaryOp(+,Id(b),IntLiteral(1))))"
        self.assertTrue(TestChecker.test(input,expect,433))

    def test_for_stmt_mismatch_2st_exp(self):
        input = """
                    void main(){
                        int a,b;
                        b = 1;
                        a = 1;
                        for(a = 1; a + 1; a = a + 1) b = b + 1;
                    }
                """
        expect = "Type Mismatch In Statement: For(BinaryOp(=,Id(a),IntLiteral(1));BinaryOp(+,Id(a),IntLiteral(1));BinaryOp(=,Id(a),BinaryOp(+,Id(a),IntLiteral(1)));BinaryOp(=,Id(b),BinaryOp(+,Id(b),IntLiteral(1))))"
        self.assertTrue(TestChecker.test(input,expect,434))

    def test_for_stmt_mismatch_3st_exp(self):
        input = """
                    void main(){
                        int a,b;
                        a = 1;
                        b = 1;
                        for(a; a < 5; b == 2) b = b + 1;
                    }
                """
        expect = "Type Mismatch In Statement: For(Id(a);BinaryOp(<,Id(a),IntLiteral(5));BinaryOp(==,Id(b),IntLiteral(2));BinaryOp(=,Id(b),BinaryOp(+,Id(b),IntLiteral(1))))"
        self.assertTrue(TestChecker.test(input,expect,435))
    
    # TEST FOR TYPE MISMATCH IN DOWHILE FUNCTION

    def test_correct_dowhile_stmt(self):
        input = """
                    void main(){
                        float a,b;
                        a = 2;
                        b = 13.5;
                        do
                        a = a + 1.5;
                        while(a < b);
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,436))

    def test_dowhile_stmt_mismatch_with_literal(self):
        input = """
                    void main(){
                        int a;
                        do 
                        a + 1;
                        while(1.5);
                    }
                """
        expect = "Type Mismatch In Statement: Dowhile([BinaryOp(+,Id(a),IntLiteral(1))],FloatLiteral(1.5))"
        self.assertTrue(TestChecker.test(input,expect,437))

    def test_dowhile_stmt_mismatch_with_Id(self):
        input = """
                    void main(){
                        string a, b[5];
                        do 
                        a = "hello";
                        while(b);
                    }
                """
        expect = "Type Mismatch In Statement: Dowhile([BinaryOp(=,Id(a),StringLiteral(hello))],Id(b))"
        self.assertTrue(TestChecker.test(input,expect,438))

    def test_dowhile_stmt_mismatch_with_unary(self):
        input = """
                    void main(){
                        int a,b;
                        do 
                        a = 1+2;
                        while(-b);
                    }
                """
        expect = "Type Mismatch In Statement: Dowhile([BinaryOp(=,Id(a),BinaryOp(+,IntLiteral(1),IntLiteral(2)))],UnaryOp(-,Id(b)))"
        self.assertTrue(TestChecker.test(input,expect,439))

    def test_dowhile_stmt_mismatch_with_binary(self):
        input = """
                    void main(){
                        int a,b,c;
                        do 
                        a = 1;
                        while(c = c + c*b);
                    }
                """
        expect = "Type Mismatch In Statement: Dowhile([BinaryOp(=,Id(a),IntLiteral(1))],BinaryOp(=,Id(c),BinaryOp(+,Id(c),BinaryOp(*,Id(c),Id(b)))))"
        self.assertTrue(TestChecker.test(input,expect,440))

    def test_dowhile_stmt_mismatch_with_funcall(self):
        input = """
                    float foo(){
                        return 12.3;
                    }
                    void main(){
                        string a, b[5];
                        do 
                        a = "hello";
                        while(foo());
                    }
                """
        expect = "Type Mismatch In Statement: Dowhile([BinaryOp(=,Id(a),StringLiteral(hello))],CallExpr(Id(foo),[]))"
        self.assertTrue(TestChecker.test(input,expect,441))

    def test_dowhile_stmt_mismatch_with_arraycell(self):
        input = """
                    void main(){
                        string a, b[5];
                        do 
                        a = "hello";
                        while(b[0]);
                    }
                """
        expect = "Type Mismatch In Statement: Dowhile([BinaryOp(=,Id(a),StringLiteral(hello))],ArrayCell(Id(b),IntLiteral(0)))"
        self.assertTrue(TestChecker.test(input,expect,442))

    # TEST FOR TYPE MISMATCH IN RETURN STATEMENT

    def test_correct_return_stmt_with_primary_type(self):
        input = """
                    int foo(int a){
                        a = a + 1;
                        return a;
                    }
                    void main(){
                        int b;
                        b = 1;
                        foo(b);
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,443))
    
    def test_correct_return_stmt_with_array_type(self):
        input = """
                    float[] foo(){
                        float a[5];
                        return a;
                    }
                    void main(){
                        foo();
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,444))

    def test_correct_return_stmt_with_arrayPointer_type(self):
        input = """
                    float[] foo(float a[]){
                        return a;
                    }
                    void main(){
                        float b[5];
                        foo(b);
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,445))

    def test_correct_return_stmt_with_void_type(self):
        input = """
                    void foo(int a[]){
                        a[1] = 1;
                        return;
                    }
                    void main(){
                        int a[5];
                        foo(a);
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,446))

    def test_type_mismatch_in_return_stmt_with_primary_type(self):
        input = """
                    string foo(int a){
                        return 5;
                    }
                    void main(){
                        int b;
                        b = 1;
                        foo(b);
                    }
                """
        expect = "Type Mismatch In Statement: Return(IntLiteral(5))"
        self.assertTrue(TestChecker.test(input,expect,447))

    def test_type_mismatch_in_return_stmt_with_arrayType_type(self):
        input = """
                    string[] foo(int a){
                        return a + 1;
                    }
                    void main(){
                        int c;
                        c = 1;
                        foo(c);
                    }
                """
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,Id(a),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,448))

    def test_type_mismatch_in_return_stmt_with_array_element_type(self):
        input = """
                    float[] foo(int a[]){
                        return a;
                    }
                    void main(){
                        int a[5];
                        foo(a);
                    }
                """
        expect = "Type Mismatch In Statement: Return(Id(a))"
        self.assertTrue(TestChecker.test(input,expect,449))

    def test_type_mismatch_in_return_stmt_with_unary_op(self):
        input = """
                    boolean foo(int a){
                        return -a;
                    }
                    void main(){
                        int a;
                        a = 1;
                        foo(a);
                    }
                """
        expect = "Type Mismatch In Statement: Return(UnaryOp(-,Id(a)))"
        self.assertTrue(TestChecker.test(input,expect,450))

    def test_type_mismatch_in_return_stmt_with_binary_op(self):
        input = """
                    string foo(int a){
                        return a*a+1;
                    }
                    void main(){
                        int a;
                        a = 1;
                        foo(a);
                    }
                """
        expect = "Type Mismatch In Statement: Return(BinaryOp(+,BinaryOp(*,Id(a),Id(a)),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,451))

    def test_type_mismatch_in_return_stmt_with_funcall(self):
        input = """
                    float fii(){
                        return 5.12;
                    }
                    int foo(){
                        return fii();
                    }
                    void main(){
                        foo();
                    }
                """
        expect = "Type Mismatch In Statement: Return(CallExpr(Id(fii),[]))"
        self.assertTrue(TestChecker.test(input,expect,452))

    def test_type_mismatch_in_return_stmt_with_arrayCell(self):
        input = """
                    string foo(int a[]){
                        return a[3];
                    }
                    void main(){
                        int a[5];
                        foo(a);
                    }
                """
        expect = "Type Mismatch In Statement: Return(ArrayCell(Id(a),IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input,expect,453))

    def test_type_mismatch_in_return_stmt_with_built_in_function(self):
        input = """
                    int foo(){
                        return getFloat();
                    }
                    void main(){
                        foo();
                    }
                """
        expect = "Type Mismatch In Statement: Return(CallExpr(Id(getFloat),[]))"
        self.assertTrue(TestChecker.test(input,expect,454))

    # TEST FOR TYPE MISMATCH IN EXPRESSION - ARRAY SUBCRIPTING

    def test_correct_index_exp_with_array_type(self):
        input = """
                    void main(){
                        int a[5];
                        a[2];
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,455))

    def test_correct_index_exp_with_arrayPointer_type(self):
        input = """
                    int foo(int b[]){
                        b[2];
                        return b[3];
                    }
                    void main(){
                        int a[5];
                        foo(a);
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,456))

    def test_correct_index_exp_with_index_as_binary_op(self):
        input = """
                    void main(){
                        int a[5];
                        a[0 + 1 + 1];
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,457))

    def test_type_mismatch_in_index_exp_with_arr(self):
        input = """
                    void main(){
                        int a;
                        a[2];
                    }
                """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input,expect,458))

    def test_type_mismatch_in_index_exp_with_index(self):
        input = """
                    void main(){
                        float b[5];
                        b[2.1];
                    }
                """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b),FloatLiteral(2.1))"
        self.assertTrue(TestChecker.test(input,expect,459))

    def test_type_mismatch_in_index_exp_with_index_as_binary(self):
        input = """
                    void main(){
                        float a;
                        a = 1.5;
                        float b[5];
                        b[a*a+1];
                    }
                """
        expect = "Type Mismatch In Expression: ArrayCell(Id(b),BinaryOp(+,BinaryOp(*,Id(a),Id(a)),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,460))

    # TEST FOR TYPE MISMATCH IN EXPRESSION - BINARY OP

    def test_coerce_int_to_float_with_binaryop(self):
        input = """
                    void main(){
                        int a,b;
                        float c;
                        a = 1; b = 2;
                        c = a + b;
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,461))

    def test_type_mismatch_in_binary_op_with_primary_type(self):
        input = """
                    void main(){
                        int a;
                        boolean b;
                        a = 1; b = false;
                        a + b;
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(+,Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,462))
    
    def test_type_mismatch_in_binary_op_with_array_type(self):
        input = """
                    void main(){
                        int a[5], b;
                        b = 1;
                        a == b + 1;
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(==,Id(a),BinaryOp(+,Id(b),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,463))

    def test_type_mismatch_in_binary_op_with_funcall(self):
        input = """
                    string foo(){
                        return "Hello World";
                    }
                    void main(){
                        int a; a = 1;
                        a <= foo();
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(<=,Id(a),CallExpr(Id(foo),[]))"
        self.assertTrue(TestChecker.test(input,expect,464))

    def test_type_mismatch_in_binary_op_with_arraycell(self):
        input = """
                    void main(){
                        int a[5];
                        float b;
                        b = 1;
                        a[5] = b + 1;
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(=,ArrayCell(Id(a),IntLiteral(5)),BinaryOp(+,Id(b),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,465))

    def test_type_mismatch_in_binary_op_with_stmt(self):
        input = """
                    void main(){
                        int a,b;
                        a = 1; b = 2;
                        if(a == true) b = b + 1;
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(==,Id(a),BooleanLiteral(true))"
        self.assertTrue(TestChecker.test(input,expect,466))

    def test_type_mismatch_in_binary_op_with_bool_variable(self):
        input = """
                    void main(){
                        boolean a,b;
                        a = true;
                        b = false;
                        a < b;
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(<,Id(a),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,467))

    def test_type_mismatch_in_binary_op_with_string_variable(self):
        input = """
                    void main(){
                        string a[6];
                        a[3] = "hello";
                        a[2] = "world";
                        a[1] = a[2] * a[3];
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(*,ArrayCell(Id(a),IntLiteral(2)),ArrayCell(Id(a),IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input,expect,468))

    # TEST FOR TYPE MISMATCH IN EXPRESSION - UNARY OP

    def test_correct_unary_op(self):
        input = """
                    void main(){
                        int a; a = 1;
                        -a;
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,469))

    def test_type_mismatch_in_unary_op_boolean(self):
        input = """
                    void main(){
                        boolean a; a= true;
                        -a;
                    }
                """
        expect = "Type Mismatch In Expression: UnaryOp(-,Id(a))"
        self.assertTrue(TestChecker.test(input,expect,470))

    def test_type_mismatch_in_unary_op_other_type(self):
        input = """
                    void main(){
                        string b;
                        b = "hello";
                        !b;
                    }
                """
        expect = "Type Mismatch In Expression: UnaryOp(!,Id(b))"
        self.assertTrue(TestChecker.test(input,expect,471))

    # TYPE MISMATCH IN EXPRESSION - ASSIGNMENT

    def test_correct_assignment(self):
        input = """
                    void main(){
                        int a; a = 1;
                        a = a + 1;
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,472))

    def test_type_mismatch_in_assignment(self):
        input = """
                    void main(){
                        int a;
                        a = "Hello";
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(a),StringLiteral(Hello))"
        self.assertTrue(TestChecker.test(input,expect,473))

    def test_type_mismatch_in_assignment_arr_type(self):
        input = """
                    void main(){
                        int a[6];
                        a = 2;
                    }
                """
        expect = "Type Mismatch In Expression: BinaryOp(=,Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input,expect,474))

    def test_coerce_int_to_float(self):
        input = """
                    void main(){
                        float b;
                        int a; a = 25;
                        b = a;
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,475))

    # TEST FOR TYPE MISMATCH IN FUNCTION CALL

    def test_correct_call_exp(self):
        input = """ 
                    int foo(){
                        return 3;
                    }
                    void main(){
                        foo();
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,476))

    def test_type_mismatch_in_call_exp_number_of_parameter(self):
        input = """ 
                    int foo(int a){
                        return 3+a;
                    }
                    void main(){
                        int a; a = 1;
                        foo(a+1,a);
                    }
                """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[BinaryOp(+,Id(a),IntLiteral(1)),Id(a)])"
        self.assertTrue(TestChecker.test(input,expect,477))

    def test_type_mismatch_in_call_exp_wrong_type_parameter(self):
        input = """ 
                    string foo(string a){
                        return a;
                    }
                    void main(){
                        boolean b; b = false;
                        foo(b);
                    }
                """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[Id(b)])"
        self.assertTrue(TestChecker.test(input,expect,478))

    def test_type_mismatch_in_call_exp_wrong_arr_type_elementtype(self):
        input = """ 
                    float foo(float a[]){
                        return a[3] + 1;
                    }
                    void main(){
                        string a[5];
                        a[3] = "hello";
                        foo(a);
                    }
                """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[Id(a)])"
        self.assertTrue(TestChecker.test(input,expect,479))

    # TEST FOR FUNCTION NOT RETURN

    def test_function_main_not_return(self):
        input = """ 
                    int main(){
                        int a;
                        a = 1;
                    }
                """
        expect = "Function main Not Return "
        self.assertTrue(TestChecker.test(input,expect,480))

    def test_function_foo_not_return(self):
        input = """ float[] foo(float b[]){
                    }
                    void main(){
                        float b[10];
                        foo(b);
                    }
                """
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input,expect,481))

    def test_function_foo_not_return_in_one_if_path(self):
        input = """ int foo(int a){
                        if(a < 10){
                            a = a + 1;
                            return a;
                        }
                        else {
                            a = a - 1;
                            a + 2;
                        }
                    }
                    void main(){
                        int a; a = 1;
                        foo(a);
                    }
                """
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input,expect,482))

    def test_function_not_return_with_for_path(self):
        input = """ int foo(int a, int b){
                        for(a; a < 10;a=a+1){
                            b = b + a;
                            return b;
                        }
                    }
                    void main(){
                        int a,b; a = 12; b = 2;
                        foo(a,b);
                    }
                """
        expect = "Function foo Not Return "
        self.assertTrue(TestChecker.test(input,expect,483))

    # TEST FOR BREAK/CONTINUE NOT IN LOOP

    def test_break_not_in_for_loop(self):
        input = """ 
                    void main(){
                        int a; a = 1;
                        for(a; a<10; a = a + 1) putStringLn("Hello") ;
                        break;
                    }
                """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,484))

    def test_break_not_in_dowhile_loop(self):
        input = """ 
                    void main(){
                        int a; a = 1;
                        do a = a + 1;
                        while(a < 10);
                        break;
                    }
                """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,485))

    def test_continue_not_in_for_loop(self):
        input = """ 
                    void main(){
                        int a;
                        a = 1;
                        for(a; a < 100; a = a + 1) a+a;
                        continue;
                    }
                """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,486))

    def test_continue_not_in_dowhile_loop(self):
        input = """ 
                    void main(){
                        int a;
                        a = 1;
                        do a=a+1;
                        while(a<3);
                        continue;
                    }
                """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,487))

    def test_correct_continue_break_in_loop(self):
        input = """ 
                    void main(){
                        int a,b;
                        a = 1; b = 200;
                        for(a; a < 100; a = a + 1){
                            b = a*a;
                            if(b < 200) break;
                        }
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,488))

    # TEST FOR NO ENTRY POINT

    def test_no_main_declaration(self):
        input = """ 
                    void foo(){
                        putStringLn("hello");
                    }
                    void hello(){
                        foo();
                    }
                """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,489))

    def test_no_main_as_function(self):
        input = """ 
                    float main;
                    void foo(){
                        main = 1;
                    }
                    void call(){
                        foo();
                    }
                """
        expect = "No Entry Point"
        self.assertTrue(TestChecker.test(input,expect,490))

    # TEST FOR UNREACHABLE FUNCTION

    def test_function_foo_not_get_invoke(self):
        input = """ int a;
                    void foo(){
                        a = 1;
                    }
                    void main(){
                        a = 2;
                    }
                """
        expect = "Unreachable Function: foo"
        self.assertTrue(TestChecker.test(input,expect,491))

    def test_function_fac_invoke_not_by_other_function(self):
        input = """ int a;
                    int fac(int a){
                        return a*fac(a-1);
                    }
                    void main(){
                        a = 1;
                    }
                """
        expect = "Unreachable Function: fac"
        self.assertTrue(TestChecker.test(input,expect,492))

    def test_function_not_get_invoke(self):
        input = """ int a;
                    int fac(int a){
                        return a*fac(a-1);
                    }
                    void main(){
                        a = 1;
                    }
                    int func(int a){
                        return fac(a)/fac(a-1);
                    }
                """
        expect = "Unreachable Function: func"
        self.assertTrue(TestChecker.test(input,expect,493))

    # TEST FOR NOT LEFT VALUE

    def test_correct_left_value(self):
        input = """ 
                    void main(){
                        int a[5];
                        a[2] = (1+2)*3/4;
                    }
                """
        expect = ""
        self.assertTrue(TestChecker.test(input,expect,494))

    def test_not_left_value_Literal(self):
        input = """ 
                    void main(){
                        1 = 2;
                    }
                """
        expect = "Not Left Value: IntLiteral(1)"
        self.assertTrue(TestChecker.test(input,expect,495))

    def test_not_left_value_unary_op(self):
        input = """ 
                    void main(){
                        boolean a;
                        a = true;
                        !a = false;
                    }
                """
        expect = "Not Left Value: UnaryOp(!,Id(a))"
        self.assertTrue(TestChecker.test(input,expect,496))

    def test_not_left_value_binary_op(self):
        input = """ 
                    void main(){
                        float a;
                        a = 4.5;
                        a + 1 = 5;
                    }
                """
        expect = "Not Left Value: BinaryOp(+,Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,497))

    def test_not_left_value_funcall(self):
        input = """ int foo(){
                        return 100;
                    }
                    void main(){
                        foo() = 99;
                    }
                """
        expect = "Not Left Value: CallExpr(Id(foo),[])"
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_not_left_value_with_type(self):
        input = """ 
                    void main(){
                        int a[5];
                        float b;
                        b = 1.5;
                        a[3] + b = 1;
                    }
                """
        expect = "Not Left Value: BinaryOp(+,ArrayCell(Id(a),IntLiteral(3)),Id(b))"
        self.assertTrue(TestChecker.test(input,expect,499))

    def test_newtest(self):
        input = Program([
                            FuncDecl(
                                Id("main"),[],IntType(),
                                Block([
                                    Id("a"),
                                    VarDecl("a",IntType()),
                                    Return(BinaryOp("/",Id("a"),IntLiteral(2)))
                                    ])
                                )
                        ])
        expect = "Undeclared Identifier: a"
        self.assertTrue(TestChecker.test(input,expect,500))