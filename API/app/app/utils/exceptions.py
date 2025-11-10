from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

def handle_integrity_error(error: IntegrityError):
    """
    Manipula erros de integridade do banco de dados e retorna uma exceção HTTP personalizada.
    """
    if 'cpf' in str(error.orig).lower():
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="Já existe um atleta cadastrado com o mesmo CPF."
        )
    elif 'categoria' in str(error.orig).lower():
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="A categoria informada já está cadastrada."
        )
    elif 'centro_treinamento' in str(error.orig).lower():
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="O centro de treinamento informado já está cadastrado."
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade no banco de dados."
        )