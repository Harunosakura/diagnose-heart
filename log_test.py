from diagnose_heart_log import dhl

@dhl.log('description')
def test_func(par1, par2):
    print par1, par2


class TestClass():
    @dhl.log('description')
    def test_method(self, par1):
        turn = dhl.turn()
        for i in range(par1):
            dhl.log_time_stamp(turn, 'log_test', 'TestClass', 'test_method', i, 'iter ' + str(i))
            print i
            #self.test_method3()

    def test_method2(self, par1):
        turn = dhl.turn()
        dhl.log_time_stamp(turn, 'log_test', 'TestClass', 'test_method', dhl.START_FUNCTION, 'function explicity')
        dhl.log_complexity(turn, 'log_test', 'TestClass', 'test_method', 'K')
        print par1
        dhl.log_time_stamp(turn, 'log_test', 'TestClass', 'test_method', dhl.END_FUNCTION, 'function explicity')
        dhl.inc_turn()

    @dhl.log('deep inside')
    def test_method3(self):
        print '---'


tc = TestClass()
test_func('v1', 'v2')
#tc.test_method2('v3')
tc.test_method(5)
#tc.test_method2('v3')
