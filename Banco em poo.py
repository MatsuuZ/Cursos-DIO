import textwrap
import re
from datetime import datetime


def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

class Transacao:
    """Interface/abstração para transações."""

    def __init__(self, valor: float):
        self.valor = float(valor)
        self.data = datetime.now()

    def registrar(self, conta):
        """Implementar nas subclasses: aplica a transação na conta e retorna bool de sucesso."""
        raise NotImplementedError("Subclasses devem implementar o método registrar.")


class Deposito(Transacao):
    """Depósito: sempre adiciona saldo se valor > 0."""

    def registrar(self, conta):
        if self.valor <= 0:
            return False, "Valor de depósito inválido."
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(f"Depósito: R$ {self.valor:.2f}")
        return True, "Depósito realizado com sucesso."


class Saque(Transacao):
    """Saque: verifica saldo, limite e número de saques da conta."""

    def registrar(self, conta):
        if self.valor <= 0:
            return False, "Valor de saque inválido."

        if self.valor > conta.saldo:
            return False, "Saldo insuficiente."

        limite = getattr(conta, "limite", None)
        if limite is not None and self.valor > limite:
            return False, "Valor excede o limite por saque."

        limite_saques = getattr(conta, "limite_saques", None)
        numero_saques = getattr(conta, "numero_saques", 0)
        if limite_saques is not None and numero_saques >= limite_saques:
            return False, "Número máximo de saques excedido."

        conta.saldo -= self.valor
        if hasattr(conta, "numero_saques"):
            conta.numero_saques += 1

        conta.historico.adicionar_transacao(f"Saque: R$ {self.valor:.2f}")
        return True, "Saque realizado com sucesso."


class Historico:
    """Armazena as transações realizadas em uma conta."""

    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, descricao: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transacoes.append(f"{timestamp} - {descricao}")

    def __str__(self):
        if not self.transacoes:
            return "Não foram realizadas movimentações."
        return "\n".join(self.transacoes)


class Conta:
    """Classe base Conta."""

    def __init__(self, agencia: str, numero: int, cliente):
        self.agencia = agencia
        self.numero = numero
        self.cliente = cliente  # referência ao objeto Cliente
        self.saldo = 0.0
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    @classmethod
    def nova_conta(cls, cliente, numero: int, agencia: str):
        """Factory para criar conta genérica (pode ser sobrescrita por subclasse)."""
        return cls(agencia=agencia, numero=numero, cliente=cliente)

    def sacar(self, valor: float):
        """Interface para realizar saque via objeto Saque."""
        transacao = Saque(valor)
        sucesso, mensagem = transacao.registrar(self)
        return sucesso, mensagem

    def depositar(self, valor: float):
        transacao = Deposito(valor)
        sucesso, mensagem = transacao.registrar(self)
        return sucesso, mensagem


class ContaCorrente(Conta):
    """Conta corrente com limite e limite de saques."""

    def __init__(self, agencia: str, numero: int, cliente, limite: float = 500.0, limite_saques: int = 3):
        super().__init__(agencia=agencia, numero=numero, cliente=cliente)
        self.limite = float(limite)
        self.limite_saques = int(limite_saques)
        self.numero_saques = 0

    @classmethod
    def nova_conta(cls, cliente, numero: int, agencia: str, limite=500.0, limite_saques=3):
        return cls(agencia=agencia, numero=numero, cliente=cliente, limite=limite, limite_saques=limite_saques)


class Cliente:
    """Classe base Cliente."""

    def __init__(self, nome: str, endereco: str = ""):
        self.nome = nome
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta: Conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta: Conta, transacao: Transacao):
        """Tenta aplicar a transação em 'conta' (desde que a conta pertença ao cliente)."""
        if conta not in self.contas:
            return False, "Conta não pertence a este cliente."

        sucesso, mensagem = transacao.registrar(conta)
        return sucesso, mensagem


class PessoaFisica(Cliente):
    """Cliente pessoa física — armazena CPF e data de nascimento."""

    def __init__(self, nome: str, cpf: str, data_nascimento: str = "", endereco: str = ""):
        super().__init__(nome=nome, endereco=endereco)
        self.cpf = re.sub(r"\D", "", cpf)
        self.data_nascimento = data_nascimento

def filtrar_usuario_por_cpf(cpf: str, usuarios: list):
    cpf_clean = re.sub(r"\D", "", cpf)
    encontrados = [u for u in usuarios if isinstance(u, PessoaFisica) and u.cpf == cpf_clean]
    return encontrados[0] if encontrados else None


def criar_usuario(usuarios: list):
    cpf = input("Informe o CPF (somente números): ").strip()
    cpf = re.sub(r"\D", "", cpf)

    if filtrar_usuario_por_cpf(cpf, usuarios):
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return None

    nome = input("Informe o nome completo: ").strip()
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ").strip()

    usuario = PessoaFisica(nome=nome, cpf=cpf, data_nascimento=data_nascimento, endereco=endereco)
    usuarios.append(usuario)
    print("\n=== Usuário criado com sucesso! ===")
    return usuario


def criar_conta_corrente(agencia: str, numero_conta: int, usuarios: list):
    cpf = input("Informe o CPF do usuário para vincular a conta: ").strip()
    cpf = re.sub(r"\D", "", cpf)

    usuario = filtrar_usuario_por_cpf(cpf, usuarios)
    if not usuario:
        print("\n@@@ Usuário não encontrado. Não foi possível criar a conta. @@@")
        return None

    conta = ContaCorrente.nova_conta(cliente=usuario, numero=numero_conta, agencia=agencia)
    usuario.adicionar_conta(conta)
    print("\n=== Conta criada com sucesso! ===")
    return conta


def listar_contas(contas: list):
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return
    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print("-" * 60)
        print(f"Agência:\t{conta.agencia}")
        print(f"C/C:\t\t{conta.numero}")
        print(f"Titular:\t{conta.cliente.nome}")
        print(f"Saldo:\t\tR$ {conta.saldo:.2f}")
        if isinstance(conta, ContaCorrente):
            print(f"Limite por saque:\tR$ {conta.limite:.2f}")
            print(f"Saques realizados:\t{conta.numero_saques}/{conta.limite_saques}")
    print("=================================================")


def encontrar_conta(contas: list, numero: int, agencia: str = None):
    for conta in contas:
        if conta.numero == numero and (agencia is None or conta.agencia == agencia):
            return conta
    return None


def flow_depositar(contas: list):
    try:
        numero = int(input("Informe o número da conta: "))
    except ValueError:
        print("\n@@@ Número de conta inválido. @@@")
        return

    conta = encontrar_conta(contas, numero, agencia=None)
    if not conta:
        print("\n@@@ Conta não encontrada. @@@")
        return

    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("\n@@@ Valor inválido. @@@")
        return

    sucesso, mensagem = conta.depositar(valor)
    if sucesso:
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print(f"\n@@@ Operação falhou! {mensagem} @@@")


def flow_sacar(contas: list):
    try:
        numero = int(input("Informe o número da conta: "))
    except ValueError:
        print("\n@@@ Número de conta inválido. @@@")
        return

    conta = encontrar_conta(contas, numero, agencia=None)
    if not conta:
        print("\n@@@ Conta não encontrada. @@@")
        return

    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("\n@@@ Valor inválido. @@@")
        return
    sucesso, mensagem = conta.sacar(valor)
    if sucesso:
        print("\n=== Saque realizado com sucesso! ===")
    else:
        print(f"\n@@@ Operação falhou! {mensagem} @@@")


def flow_exibir_extrato(contas: list):
    try:
        numero = int(input("Informe o número da conta: "))
    except ValueError:
        print("\n@@@ Número de conta inválido. @@@")
        return

    conta = encontrar_conta(contas, numero, agencia=None)
    if not conta:
        print("\n@@@ Conta não encontrada. @@@")
        return

    print("\n================ EXTRATO ================")
    print(conta.historico)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    contas = []
    usuarios = []

    while True:
        opcao = menu()

        if opcao == "d":
            flow_depositar(contas)

        elif opcao == "s":
            flow_sacar(contas)

        elif opcao == "e":
            flow_exibir_extrato(contas)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_nova_conta = len(contas) + 1
            conta = criar_conta_corrente(AGENCIA, numero_nova_conta, usuarios)
            if conta:
                contas.append(conta)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("\nObrigado por utilizar nosso sistema. Até logo!\n")
            break

        else:
            print("\nOperação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
