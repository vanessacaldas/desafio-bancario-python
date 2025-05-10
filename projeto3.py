from abc import ABC, abstractmethod 
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realiza_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta) 

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        if valor > self.saldo:
            print("Operação falou! Saldo insuficiente.")
            return False
     
        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso!")
            return True
    
        else:
            print("Operação falou! Valor inválido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:    
            self._saldo += valor
            print(" Depósito realizado com sucesso!")
            return True
        
        else:
         print("Operação falhou! Valor inválido.")
         return False
        
        return True

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500.0, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques
        
    def sacar(self, valor):
        saque = [t for t in self.historico.transacoes if t["tipo"] == Saque.__name__]     
        if len(saques) >= self._limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False

        elif valor >  self._limite:
            print("Operação falhou!O valor do saque excede o limite.")
            return False
            
        else:
           return super().sacar(valor)
    

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t {self.cliente.nome}
        """
    
class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
   
    @abstractmethod
    def registrar(self, conta):
        pass

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self._valor)

        if   sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"Depósito de R$ {self._valor:.2f} em {datetime.now()}"
        

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
  
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self._valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

    def __str__(self):
        return f"Saque de R$ {self._valor:.2f} em {datetime.now()}"

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes    

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.nowo().strftime("%d-%m-%y %H:%M:%s")
            }
            )

    










