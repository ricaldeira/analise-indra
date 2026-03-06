#!/bin/bash
# Script para visualizar logs em tempo real

echo "=== VISUALIZADOR DE LOGS DO SISTEMA ANÁLISE INDRA ==="
echo ""
echo "Opções:"
echo "1) Ver logs em tempo real (tail -f)"
echo "2) Ver últimas 50 linhas"
echo "3) Ver logs de erros apenas"
echo "4) Ver logs de processamento XLS"
echo "5) Limpar arquivo de log"
echo ""

read -p "Escolha uma opção (1-5): " opcao

case $opcao in
    1)
        echo "=== LOGS EM TEMPO REAL (Ctrl+C para sair) ==="
        tail -f logs/processamento.log
        ;;
    2)
        echo "=== ÚLTIMAS 50 LINHAS DO LOG ==="
        tail -50 logs/processamento.log
        ;;
    3)
        echo "=== LOGS DE ERRO ==="
        grep "ERROR" logs/processamento.log | tail -20
        ;;
    4)
        echo "=== LOGS DE PROCESSAMENTO XLS ==="
        grep "PROCESSAMENTO XLS" logs/processamento.log -A 5 -B 5
        ;;
    5)
        echo "=== LIMPANDO ARQUIVO DE LOG ==="
        read -p "Tem certeza que deseja limpar o log? (s/n): " confirm
        if [ "$confirm" = "s" ]; then
            > logs/processamento.log
            echo "Log limpo com sucesso!"
        else
            echo "Operação cancelada."
        fi
        ;;
    *)
        echo "Opção inválida!"
        ;;
esac