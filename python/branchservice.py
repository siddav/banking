import branch_pb2
import branch_pb2_grpc
# service related to branch-branch communications
class BranchService(branch_pb2_grpc.SyncAccountServicer):
    def __init__(self, account):
        self.account = account

    def PropogateDeposit(self, request, context):
        amount = request.amount
        self.account.deposit(amount)
        return branch_pb2.SyncAccountResponse(message="success")

    def PropogateWithdraw(self, request, context):
        amount = request.amount
        self.account.withdraw(amount)
        return branch_pb2.SyncAccountResponse(message="success")