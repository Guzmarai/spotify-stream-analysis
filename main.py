# main.py
from src import cleanup


def main():
    print("--- Iniciando Pipeline de Dados ---")

    try:
        # Chama a função do script de tratamento
        cleanup.run_cleanup()
        print("--- Pipeline finalizado com sucesso ---")
    except ValueError as vE:
        print(f"Número inválido durante a execução: {vE}")
    except ZeroDivisionError as zE:
        print(f"Erro de divisão por zero durante a execução: {zE}")
    except KeyboardInterrupt:
        print("--- Pipeline interrompido pelo usuário ---")  
    except Exception as e:  # noqa: BLE001
        print(f"Ocorreu um erro inesperado: {e}")


if __name__ == "__main__":
    main()
