import logging
import random
import json
import os
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Variáveis globais para o comando /aleatorio
random_number = None
last_generated_time = 0  # Timestamp inicial

def carregar_saldos():
    if os.path.exists('saldos.json'):
        with open('saldos.json', 'r') as f:
            return json.load(f)
    else:
        return {}

def salvar_saldos(saldos):
    with open('saldos.json', 'w') as f:
        json.dump(saldos, f, indent=4)
    logger.info("Saldos salvos no arquivo.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Comando /start recebido")
    await update.message.reply_text(
        """Wsp vermes, comandos por enquanto:
- /start - Inicia o bot
- /escolher - Escolhe um verme aleatório
- /dbl - Escolhe uma tag aleatória do DBL
- /gambling - LETS GO GAMBLING
- /forca - Desativado por enquanto
- /saldo - Mostra o saldo atual (o saldo é salvo msm após o bot ser reiniciado)
- /coinflip - LETS GO GAMBLING
- /dice - LETS GO GAMBLING
- /temu - Mostra a quantidade de trabalhadores (kids) que fugiram da temu nos últimos 10 minutos
- /pagar - Paga alguém
- /apostar - Auto explicativo ne diabo"""
    )

async def escolher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pessoas = context.args if context.args else ['isma', 'diogo', 'andre', 'gomes']
    escolhida = random.choice(pessoas)
    logger.info(f"Escolhido: {escolhida}")
    await update.message.reply_text(f'Nego escolhido: {escolhida}')

async def dbl(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    tags = context.args if context.args else [
        'absorption', 'android', 'angel', 'daima', 'DB', 'event exclusive', 'frieza force',
        'fusion', 'fusion warrior', 'future', 'GT', 'ginyu force', 'girls', 'god ki',
        'god of destruction', 'hera clan', 'hybrid saiyan', 'kids', 'legends road',
        'lineage of evil', 'merging', 'minion', 'namekian', 'otherworld warrior', 'potara',
        'powerful opponent', 'regeneration', 'rival universe', 'saiyan', 'shadow dragon',
        'son family', 'super saiyan', 'super saiyan 2', 'super saiyan 3', 'super saiyan 4',
        'super saiyan god', 'super saiyan god ss', 'super saiyan rosé', 'super warrior',
        'team bardock', 'transforming warrior', 'turles crusher corps', 'twins', 'universe 2',
        'universe 4', 'universe 6', 'universe 9', 'universe 11', 'universe rep',
        'vegeta clan', 'weapon wielder'
    ]
    tag = random.choice(tags)
    logger.info(f"Tag escolhida: {tag}")
    await update.message.reply_text(f'Tag: {tag}')

async def pagar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    saldos = carregar_saldos()
    user_id = str(update.message.from_user.id)  # ID do utilizador que chama o comando

    if len(context.args) < 2:
        await update.message.reply_text("Usa assim: /pagar NomeDoAlvo valor")
        return

    alvo_nome = context.args[0]  # O nome completo do alvo
    try:
        valor = int(context.args[1])  # Tenta converter o segundo argumento para número
    except ValueError:
        await update.message.reply_text("O valor deve ser um número.")
        return

    if valor <= 0:
        await update.message.reply_text("Valor inválido.")
        return

    # Procurar o ID do alvo no arquivo de saldos pelo nome
    alvo_id = None
    for key, value in saldos.items():
        # Aqui verificamos o nome do utilizador
        if value.get("nome") == alvo_nome:  # Supondo que "nome" seja a chave para o nome do alvo
            alvo_id = key
            break

    if not alvo_id:
        await update.message.reply_text(f"Não encontrei nenhum utilizador com o nome {alvo_nome}.")
        return

    # Se o utilizador não estiver no arquivo de saldos, inicializa com saldo 100
    if user_id not in saldos:
        saldos[user_id] = {"nome": update.message.from_user.full_name, "saldo": 100}
    if alvo_id not in saldos:
        saldos[alvo_id] = {"nome": alvo_nome, "saldo": 100}

    # Verifica se o utilizador tem saldo suficiente
    if saldos[user_id]["saldo"] < valor:
        await update.message.reply_text("Não tens saldo suficiente.")
        return

    # Realiza o pagamento
    saldos[user_id]["saldo"] -= valor
    saldos[alvo_id]["saldo"] += valor
    salvar_saldos(saldos)

    await update.message.reply_text(f"Pagaste {valor}€ a {alvo_nome}.")

MAX_VALOR_APOSTA = 10000  # Limite máximo para a aposta

async def apostar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    saldos = carregar_saldos()  # Carrega os saldos do arquivo JSON
    user_id = str(update.message.from_user.id)  # ID do utilizador que chama o comando

    if len(context.args) < 1:
        await update.message.reply_text("Usa assim: /apostar <valor da aposta>")
        return

    try:
        valor = int(context.args[0])  # O primeiro argumento é o valor da aposta
    except ValueError:
        await update.message.reply_text("O valor da aposta deve ser um número.")
        return

    if valor <= 0:
        await update.message.reply_text("O valor da aposta deve ser maior que 0.")
        return

    # Verifica se o utilizador tem saldo suficiente para a aposta
    if saldos[user_id]["saldo"] < valor:
        await update.message.reply_text("Ta sem saldo pra isso.")
        return

    # Calcula a probabilidade com base no valor da aposta
    sorteio = random.randint(1, 100)

    if sorteio <= 40:  # 40% de chance de ganhar o dobro
        saldos[user_id]["saldo"] += valor
        await update.message.reply_text(f"Ganhaste o dobro +{valor}€. Saldo: {saldos[user_id]['saldo']}€")
    elif sorteio <= 80:  # 40% de chance de perder
        saldos[user_id]["saldo"] -= valor
        if saldos[user_id]["saldo"] < 0:
            saldos[user_id]["saldo"] = 0
        await update.message.reply_text(f"Perdeste, L -{valor}€. Saldo: {saldos[user_id]['saldo']}€")
    else:  # 20% de chance de nada acontecer
        await update.message.reply_text(f"Nada aconteceu. Saldo: {saldos[user_id]['saldo']}€")

    salvar_saldos(saldos)  # Salva os saldos atualizados no arquivo JSON

async def saldo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    saldos = carregar_saldos()

    if user_id not in saldos:
        saldos[user_id] = {"nome": update.message.from_user.full_name, "saldo": 100}

    await update.message.reply_text(f"saldo atual: {saldos[user_id]['saldo']}€.")

async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    saldos = carregar_saldos()

    bet = 10
    if saldos[user_id] < bet:
        await update.message.reply_text("Ta sem dinheiro mn")
        return

    result = random.choice(["cara", "coroa"])
    choice = random.choice(["cara", "coroa"])

    if result == choice:
        saldos[user_id] += bet
        await update.message.reply_text(f"Escolheste {choice} e deu {result}. Ganhaste 10€! Saldo: {saldos[user_id]}€. ")
    else:
        saldos[user_id] -= bet
        await update.message.reply_text(f"Escolheste {choice} e deu {result}. Perdeste 10€. Saldo: {saldos[user_id]}€.")

    salvar_saldos(saldos)

async def dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.message.from_user.id)
    saldos = carregar_saldos()

    bet = 10
    if saldos[user_id] < bet:
        await update.message.reply_text("Ta sem dinheiro mn")
        return

    result = random.randint(1, 6)
    if result > 3:
        saldos[user_id] += bet
        await update.message.reply_text(f"Vas a rolar o dado... e deu {result}. Ganhaste 10€! Saldo: {saldos[user_id]}€. ")
    else:
        saldos[user_id] -= bet
        await update.message.reply_text(f"Vas a rolar o dado... e deu {result}. Perdeste 10€. Saldo: {saldos[user_id]}€.")

    salvar_saldos(saldos)

def main() -> None:
    application = Application.builder().token('7826080755:AAFkDiTFkWC1w24ueEYfPJvEr3EEftevTGA').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("escolher", escolher))
    application.add_handler(CommandHandler("dbl", dbl))
    application.add_handler(CommandHandler("pagar", pagar))
    application.add_handler(CommandHandler("apostar", apostar))
    application.add_handler(CommandHandler("saldo", saldo))
    application.add_handler(CommandHandler("coinflip", coinflip))
    application.add_handler(CommandHandler("dice", dice))

    application.run_polling()

if __name__ == '__main__':
    main()