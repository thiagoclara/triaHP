import json
import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ChatJoinRequestHandler,
    ContextTypes,
    filters,
)

# ================= CONFIG =================
TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 1130170420

# IDs que podem refazer a triagem para testes
IDS_TESTE = [8672397104]

GRUPO_TRIAGEM_ID = -1003827066177
GRUPO_OFICIAL_ID = -1003553956365

BOT_USERNAME = "Expresso_Hogwarts_Bot"

NOME_GUARDIA = "🦉 Coruja da Biblioteca"

ARQUIVO_DADOS = "triagem_dados.json"

config_acesso = {
    "imagem_file_id": None,
    "mensagem": (
        "✨📜 Perfil verificado com sucesso!\n\n"
        "A Biblioteca de Hogwarts está pronta para receber você.\n\n"
        "Clique no botão abaixo para entrar.\n\n"
        "⚠️ Este acesso é único, não deve ser compartilhado e será removido após o uso."
    ),
    "texto_botao": "🏰 Entrar na Biblioteca de Hogwarts"
}

# ================= DADOS =================
usuarios = {}

# IMPORTANTE:
# fichas_alunos = SOMENTE fichas novas aguardando avaliação
fichas_alunos = {}

alunos_pendentes = {}
alunos_liberados = {}
alunos_reprovados = {}
alunos_entraram_triagem = {}
links_enviados = {}
historico_links = {}
alunos_no_oficial = {}

# ================= PERGUNTAS DA TRIAGEM =================

perguntas = [
    {
        "pergunta": "📚 Qual gênero literário você mais gosta de ler?",
        "opcoes": [
            "💕 Romance",
            "🧙 Fantasia",
            "🔪 Suspense/Terror",
            "🎭 Drama",
            "🌈 Gosto de vários gêneros"
        ]
    },

    {
        "pergunta": "💕 Como você prefere o desenvolvimento de um romance?",
        "opcoes": [
            "🐢 Bem lento e detalhado",
            "🔥 Intenso desde o começo",
            "⚖️ Um pouco dos dois",
            "💫 O romance pode ser secundário"
        ]
    },

    {
        "pergunta": "🔥 Você gosta de livros com cenas hot/18+?",
        "opcoes": [
            "🔥 Sim, gosto bastante",
            "💕 Sim, mas sem exageros",
            "📖 Prefiro quando não tem",
            "🚫 Não gosto"
        ]
    },

    {
        "pergunta": "🖤 O que você acha de Dark Romance?",
        "opcoes": [
            "🖤 Adoro",
            "🥀 Gosto, mas depende da história",
            "🤔 Nunca li",
            "🚫 Não faz meu estilo"
        ]
    },

    {
        "pergunta": "🧙 Você gosta de histórias com magia, criaturas sobrenaturais ou mundos fantásticos?",
        "opcoes": [
            "✨ Amo fantasia",
            "🪄 Gosto bastante",
            "🌙 Às vezes",
            "📚 Prefiro histórias realistas"
        ]
    },

    {
        "pergunta": "🔪 Qual dessas opções mais combina com você?",
        "opcoes": [
            "🔍 Mistérios e investigação",
            "👻 Terror e medo",
            "⚡ Suspense e tensão",
            "💕 Prefiro romance e drama"
        ]
    },

    {
        "pergunta": "⚔️ O que você acha de protagonistas moralmente duvidosos ou anti-heróis?",
        "opcoes": [
            "🖤 Adoro personagens assim",
            "🔥 Gosto quando são bem escritos",
            "🤔 Depende do personagem",
            "👑 Prefiro protagonistas bonzinhos"
        ]
    },

    {
        "pergunta": "💘 Qual dinâmica de romance mais chama sua atenção?",
        "opcoes": [
            "🔥 Enemies to Lovers",
            "⚡ Rivals to Lovers",
            "💍 Fake Dating",
            "🫶 Friends to Lovers",
            "💫 Qualquer uma, se a história for boa"
        ]
    },

    {
        "pergunta": "🥀 Você gosta de histórias emocionalmente intensas?",
        "opcoes": [
            "😭 Amo sofrer com os personagens",
            "💔 Gosto bastante",
            "🌷 Prefiro algo equilibrado",
            "😊 Prefiro histórias leves"
        ]
    },

    {
        "pergunta": "⚡ O quanto você gosta de plot twists?",
        "opcoes": [
            "🤯 Quero ser enganado até a última página",
            "🔥 Quanto mais reviravoltas, melhor",
            "✨ Algumas são suficientes",
            "📖 Prefiro histórias previsíveis"
        ]
    },

    {
        "pergunta": "👑 Qual tipo de protagonista você prefere?",
        "opcoes": [
            "🖤 Anti-herói poderoso",
            "👑 Pessoa rica/poderosa",
            "🌷 Pessoa comum e identificável",
            "🧙 Herói ou heroína de fantasia",
            "💫 Não tenho preferência"
        ]
    },

    {
        "pergunta": "🕰️ Você gosta de livros ambientados em outras épocas?",
        "opcoes": [
            "👑 Amo romances de época",
            "📜 Gosto bastante",
            "🤔 Às vezes",
            "🏙️ Prefiro histórias atuais"
        ]
    },

    {
        "pergunta": "🌎 Você gosta de conhecer outras culturas através dos livros?",
        "opcoes": [
            "🌎 Sim, adoro",
            "📚 Gosto bastante",
            "✨ Depende do livro",
            "🏠 Prefiro histórias mais familiares"
        ]
    },

    {
        "pergunta": "📖 Você prefere...",
        "opcoes": [
            "📕 Livro único",
            "📚 Duologia",
            "📚📚 Trilologias e séries",
            "🏰 Séries enormes com vários livros",
            "💫 Não tenho preferência"
        ]
    },

    {
        "pergunta": "🐢 Qual ritmo de leitura você prefere?",
        "opcoes": [
            "⚡ Rápido e viciante",
            "🔥 Ritmo médio",
            "🐢 Lento e detalhado",
            "📖 Depende da história"
        ]
    },

    {
        "pergunta": "📚 O que mais faz você continuar lendo um livro?",
        "opcoes": [
            "💕 Romance",
            "🧩 Mistério e curiosidade",
            "⚔️ Ação e aventura",
            "🥀 Emoções e personagens",
            "🌎 O universo e a construção da história"
        ]
    },

    {
        "pergunta": "🚪 Quando um livro começa devagar, você...",
        "opcoes": [
            "⏳ Dou bastante tempo para a história desenvolver",
            "📖 Continuo se os personagens forem bons",
            "🤔 Leio mais alguns capítulos",
            "🚪 Abandono rapidamente"
        ]
    },

    {
        "pergunta": "🔎 Como você costuma escolher sua próxima leitura?",
        "opcoes": [
            "⭐ Pela avaliação/recomendação",
            "🖼️ Pela capa e sinopse",
            "👤 Pela indicação de alguém",
            "📚 Pelo autor",
            "🎲 Escolho aleatoriamente"
        ]
    },

    {
        "pergunta": "⏳ Quando você recebe um livro que estava esperando, você...",
        "opcoes": [
            "🚀 Começo imediatamente",
            "📖 Começo assim que tenho tempo",
            "📚 Coloco na lista de próximas leituras",
            "🐢 Leio quando estiver no clima"
        ]
    },

    {
        "pergunta": "🤝 Para finalizar: você entende e respeita que nem todos os livros estarão disponíveis no grupo?",
        "opcoes": [
            "💚 Sim, com certeza!",
            "📚 Sim, entendo que existem limites",
            "🤔 Sim, mas posso perguntar por alternativas",
            "❤️ Claro, respeito as regras da biblioteca"
        ]
    }
]

# ================= SALVAR / CARREGAR =================

def salvar_dados():
    dados = {
        "usuarios": usuarios,
        "fichas_alunos": fichas_alunos,
        "alunos_pendentes": alunos_pendentes,
        "alunos_liberados": alunos_liberados,
        "alunos_reprovados": alunos_reprovados,
        "alunos_entraram_triagem": alunos_entraram_triagem,
        "links_enviados": links_enviados,
        "historico_links": historico_links,
        "alunos_no_oficial": alunos_no_oficial,
        "config_acesso": config_acesso,
    }

    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(
            dados,
            f,
            ensure_ascii=False,
            indent=4
        )


def carregar_dados():

    global usuarios, fichas_alunos, alunos_pendentes
    global alunos_liberados, alunos_reprovados
    global alunos_entraram_triagem, links_enviados
    global historico_links, alunos_no_oficial
    global config_acesso


    if not os.path.exists(ARQUIVO_DADOS):
        salvar_dados()
        return


    try:
        with open(
            ARQUIVO_DADOS,
            "r",
            encoding="utf-8"
        ) as f:
            dados = json.load(f)

    except Exception:
        salvar_dados()
        return


    usuarios.update(
        dados.get("usuarios", {})
    )

    fichas_alunos.update(
        dados.get("fichas_alunos", {})
    )

    alunos_pendentes.update(
        dados.get("alunos_pendentes", {})
    )

    alunos_liberados.update(
        dados.get("alunos_liberados", {})
    )

    alunos_reprovados.update(
        dados.get("alunos_reprovados", {})
    )

    alunos_entraram_triagem.update(
        dados.get("alunos_entraram_triagem", {})
    )

    links_enviados.update(
        dados.get("links_enviados", {})
    )

    historico_links.update(
        dados.get("historico_links", {})
    )

    alunos_no_oficial.update(
        dados.get("alunos_no_oficial", {})
    )

    config_acesso.update(
        dados.get("config_acesso", {})
    )

def k(user_id):
    return str(user_id)


def ficha_do_aluno(user_key):
    if user_key in fichas_alunos:
        return fichas_alunos[user_key]

    if user_key in alunos_pendentes:
        return alunos_pendentes[user_key].get(
            "ficha",
            "Ficha não encontrada."
        )

    if user_key in alunos_liberados:
        return alunos_liberados[user_key].get(
            "ficha",
            "Ficha não encontrada."
        )

    if user_key in alunos_reprovados:
        return alunos_reprovados[user_key].get(
            "ficha",
            "Ficha não encontrada."
        )

    return "Ficha não encontrada."


def tem_triagem_bloqueada(user_key):
    return (
        user_key in fichas_alunos
        or user_key in alunos_pendentes
        or user_key in alunos_liberados
        or user_key in alunos_reprovados
    )

async def esta_na_triagem(context, user_id):
    try:
        membro = await context.bot.get_chat_member(
            chat_id=GRUPO_TRIAGEM_ID,
            user_id=user_id
        )

        return membro.status in [
            "member",
            "administrator",
            "creator"
        ]

    except Exception as erro:
        print(
            f"Erro ao verificar membro da triagem "
            f"({user_id}): {erro}"
        )
        return False

async def texto_perfil(context, user_id):

    try:
        tem_foto, tem_usuario, username = await verificar_perfil(
            context,
            user_id
        )

    except Exception:
        tem_foto, tem_usuario, username = False, False, None

    username_txt = f"@{username}" if tem_usuario else "Sem usuário"

    perfil_link = f"tg://user?id={user_id}"

    foto_txt = "Sim" if tem_foto else "Não"

    return (
        f"🆔 ID Telegram: {user_id}\n"
        f"🔗 Usuário: {username_txt}\n"
        f"👁 Perfil: {perfil_link}\n"
        f"📸 Foto no perfil: {foto_txt}\n"
    )
    
# ================= TECLADO PROFESSORES =================

def teclado_professores():

    teclado = [
        [
            "📜 Fichas Aguardando",
            "⚠️ Alunos Pendentes"
        ],
        [
            "✅ Alunos Aprovados",
            "❌ Alunos Reprovados"
        ],
        [
            "🧍 Entraram na Triagem",
            "🏰 Entraram no Oficial"
        ],
        [
            "🔗 Links Enviados",
            "⚙️ Personalizar Acesso"
        ]
    ]

    return ReplyKeyboardMarkup(
        teclado,
        resize_keyboard=True
    )

def teclado_personalizar():
    return ReplyKeyboardMarkup(
        [
            ["🖼 Alterar imagem do acesso"],
            ["✏️ Alterar mensagem do acesso"],
            ["🔘 Alterar texto do botão"],
            ["👁 Visualizar acesso"],
            ["🔙 Voltar"]
        ],
        resize_keyboard=True
    )

# ================= START =================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    user_key = k(user_id)

    # ================= ADMIN =================

    if user_id == ADMIN_ID:

        context.user_data.clear()

        await update.message.reply_text(
            f"🏰✨ Bem-vinda à Sala dos Professores!\n\n"
            f"{NOME_GUARDIA} está pronta para organizar as fichas dos alunos.",
            reply_markup=teclado_professores()
        )

        return

    # ================= VERIFICAR SE ESTÁ NA TRIAGEM =================

    esta_no_grupo = await esta_na_triagem(
        context,
        user_id
    )

    if not esta_no_grupo:

        await update.message.reply_text(
            f"{NOME_GUARDIA}\n\n"
            "⚠️ Acesso à Triagem Literária não autorizado.\n\n"
            "🏰 Antes de iniciar sua jornada, você precisa "
            "entrar no grupo Expresso Hogwarts.\n\n"
            "🚂✨ Depois de entrar no grupo de triagem, "
            "utilize o botão enviado pela Coruja da Biblioteca "
            "para iniciar sua Triagem Literária."
        )

        return

    # ================= VERIFICAR SE JÁ FEZ TRIAGEM =================

    if user_id not in IDS_TESTE and tem_triagem_bloqueada(user_key):

        if user_key in fichas_alunos:

            await update.message.reply_text(
                "📜 Sua triagem já foi finalizada e está "
                "aguardando avaliação dos professores."
            )

            return

        if user_key in alunos_pendentes:

            await update.message.reply_text(
                "⚠️ Sua ficha está pendente.\n\n"
                "Corrija foto/usuário e envie /verificar."
            )

            return

        if user_key in alunos_liberados:

            await update.message.reply_text(
                "✅ Você já foi aprovado e liberado "
                "para a Biblioteca de Hogwarts."
            )

            return

        if user_key in alunos_reprovados:

            await update.message.reply_text(
                "❌ Sua triagem já foi avaliada.\n\n"
                "Aguarde orientação dos professores."
            )

            return

    # ================= INICIAR TRIAGEM =================

    usuarios[user_key] = {
        "etapa": "nome"
    }

    alunos_entraram_triagem.setdefault(
        user_key,
        {
            "nome": update.message.from_user.first_name,
            "username": update.message.from_user.username or "Sem usuário",
            "id": user_id,
            "status": "Começou a triagem"
        }
    )

    alunos_entraram_triagem[user_key]["status"] = (
        "Começou a triagem"
    )

    salvar_dados()

    await update.message.reply_text(
        f"{NOME_GUARDIA}\n\n"
        "🧪✨ Triagem Literária iniciada!\n\n"
        "Antes de receber o acesso ao grupo oficial "
        "Biblioteca de Hogwarts 🏰📖, "
        "responda sua avaliação.\n\n"
        "✨ Primeiro, diga seu nome:"
    )

# ================= NOVO MEMBRO NA TRIAGEM / OFICIAL =================
async def novo_membro(update: Update, context: ContextTypes.DEFAULT_TYPE):

    chat_id = update.effective_chat.id

    if chat_id == GRUPO_TRIAGEM_ID:

        for membro in update.message.new_chat_members:

            if membro.is_bot:
                continue

            user_id = membro.id
            user_key = k(user_id)
            nome = membro.first_name

            alunos_entraram_triagem[user_key] = {
                "nome": nome,
                "username": membro.username or "Sem usuário",
                "id": user_id,
                "status": "Entrou na triagem, mas ainda não finalizou"
            }

            salvar_dados()

            keyboard = [[
                InlineKeyboardButton(
                    "🧪 Fazer Triagem Literária",
                    url=f"https://t.me/{BOT_USERNAME}?start=triagem"
                )
            ]]

            await context.bot.send_message(
                chat_id=GRUPO_TRIAGEM_ID,
                text=(
                    f"🦉✨ Seja bem-vindo(a), {nome}!\n\n"
                    "Você chegou à Plataforma 9¾ 🚂✨📖\n\n"
                    "Este é o grupo de entrada para quem deseja fazer parte do nosso grupo oficial:\n\n"
                    "🏰📖 Biblioteca de Hogwarts\n\n"
                    "📌 Requisitos obrigatórios:\n"
                    "• Ter uma imagem/foto no perfil\n"
                    "• Ter um usuário visível no Telegram, exemplo: @seunome\n\n"
                    "Clique no botão abaixo para fazer sua Triagem Literária:"
                ),
                reply_markup=InlineKeyboardMarkup(keyboard)
            )


    elif chat_id == GRUPO_OFICIAL_ID:

        for membro in update.message.new_chat_members:

            user_id = membro.id
            user_key = k(user_id)

            passou_pela_triagem = (
                user_key in alunos_liberados
                or user_key in alunos_pendentes
                or user_key in alunos_reprovados
                or user_key in fichas_alunos
                or user_key in historico_links
            )

            alunos_no_oficial[user_key] = {
                "nome": membro.first_name,
                "username": membro.username or "Sem usuário",
                "id": user_id,
                "status": "Entrou após triagem" if passou_pela_triagem else "Entrou sem passar pela triagem"
            }

            if user_key in historico_links:
                historico_links[user_key]["status"] = "Entrou no grupo oficial"

            if user_key in alunos_liberados:
                alunos_liberados[user_key]["status"] = "Entrou no grupo oficial"

            if user_key in links_enviados:

                try:

                    registro_link = links_enviados[user_key]

                    message_id = registro_link.get(
                        "message_id"
                    )

                    if message_id:

                        await context.bot.delete_message(
                            chat_id=user_id,
                            message_id=message_id
                        )

                except Exception as erro:

                    print(
                        "Erro ao apagar link do PV:",
                        erro
                    )

                links_enviados.pop(
                    user_key,
                    None
                )

            salvar_dados()

# ================= PERSONALIZAÇÃO DO ACESSO =================
async def processar_personalizacao_admin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if update.message.from_user.id != ADMIN_ID:
        return False

    modo = context.user_data.get("modo_admin")

    if not modo:
        return False

    texto = update.message.text.strip() if update.message.text else ""


    if modo == "alterar_imagem_acesso":

        if update.message.photo:

            config_acesso["imagem_file_id"] = update.message.photo[-1].file_id

            salvar_dados()

            context.user_data.pop("modo_admin", None)

            await update.message.reply_text(
                "✅ Imagem do acesso atualizada.",
                reply_markup=teclado_personalizar()
            )

            return True


        if texto.lower() == "remover":

            config_acesso["imagem_file_id"] = None

            salvar_dados()

            context.user_data.pop("modo_admin", None)

            await update.message.reply_text(
                "✅ Imagem removida do acesso.",
                reply_markup=teclado_personalizar()
            )

            return True


        await update.message.reply_text(
            "⚠️ Envie uma imagem ou digite remover."
        )

        return True



    if modo == "alterar_mensagem_acesso":

        if not texto:

            await update.message.reply_text(
                "⚠️ Envie uma mensagem em texto."
            )

            return True


        config_acesso["mensagem"] = texto

        salvar_dados()

        context.user_data.pop("modo_admin", None)

        await update.message.reply_text(
            "✅ Mensagem do acesso atualizada.",
            reply_markup=teclado_personalizar()
        )

        return True



    if modo == "alterar_botao_acesso":

        if not texto:

            await update.message.reply_text(
                "⚠️ Envie o texto do botão."
            )

            return True


        config_acesso["texto_botao"] = texto

        salvar_dados()

        context.user_data.pop("modo_admin", None)

        await update.message.reply_text(
            "✅ Texto do botão atualizado.",
            reply_markup=teclado_personalizar()
        )

        return True


    return False



async def enviar_preview_acesso(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    keyboard = [[
        InlineKeyboardButton(
            config_acesso["texto_botao"],
            url="https://t.me/preview"
        )
    ]]

    caption = (
        f"{NOME_GUARDIA}\n\n"
        f"{config_acesso['mensagem']}"
    )


    if config_acesso.get("imagem_file_id"):

        await update.message.reply_photo(
            photo=config_acesso["imagem_file_id"],
            caption=caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            protect_content=True
        )


    else:

        await update.message.reply_text(
            caption,
            reply_markup=InlineKeyboardMarkup(keyboard),
            protect_content=True
        )

    # ================= LISTAS =================

async def mostrar_lista_fichas(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not fichas_alunos:
        await update.message.reply_text(
            "📜 Nenhuma ficha aguardando avaliação."
        )
        return

    keyboard = []

    for uid in fichas_alunos:

        nome = usuarios.get(uid, {}).get("nome", str(uid))

        keyboard.append([
            InlineKeyboardButton(
                f"👤 {nome}",
                callback_data=f"ver_ficha_{uid}"
            )
        ])


    await update.message.reply_text(
        "📜 Fichas Aguardando Avaliação\n\nEscolha uma ficha:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def mostrar_pendentes(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not alunos_pendentes:

        await update.message.reply_text(
            "⚠️ Nenhum aluno pendente no momento.",
            reply_markup=teclado_professores()
        )

        return


    keyboard = []

    for uid in alunos_pendentes:

        nome = alunos_pendentes[uid].get("nome", str(uid))

        keyboard.append([
            InlineKeyboardButton(
                f"⚠️ {nome}",
                callback_data=f"ver_pendente_{uid}"
            )
        ])


    await update.message.reply_text(
        "⚠️ Alunos Pendentes\n\n"
        "Aqui ficam alunos que precisam corrigir foto/usuário. "
        "Você também pode liberar manualmente se conhecer a pessoa.\n\n"
        "Escolha um aluno:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def mostrar_liberados(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not alunos_liberados:

        await update.message.reply_text(
            "✅ Nenhum aluno aprovado/liberado ainda.",
            reply_markup=teclado_professores()
        )

        return


    keyboard = []

    for uid, info in alunos_liberados.items():

        nome = info.get("nome", str(uid))

        keyboard.append([
            InlineKeyboardButton(
                f"✅ {nome}",
                callback_data=f"ver_aprovado_{uid}"
            )
        ])


    await update.message.reply_text(
        "✅ Alunos Aprovados / Liberados\n\n"
        "Aqui ficam somente alunos aprovados.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )



async def mostrar_entradas_triagem(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    nao_finalizaram = {
        uid: info
        for uid, info in alunos_entraram_triagem.items()
        if uid not in fichas_alunos
        and uid not in alunos_pendentes
        and uid not in alunos_liberados
        and uid not in alunos_reprovados
    }


    if not nao_finalizaram:

        await update.message.reply_text(
            "🧍 Nenhum aluno parado na triagem.\n\n"
            "Aqui só aparecem pessoas que entraram na triagem, mas ainda não finalizaram a prova.",
            reply_markup=teclado_professores()
        )

        return


    texto = (
        "🧍 Entraram na Triagem e Ainda Não Finalizaram\n\n"
    )


    for uid, info in nao_finalizaram.items():

        username = info.get(
            "username",
            "Sem usuário"
        )

        texto += (
            f"👤 {info.get('nome', 'Sem nome')}\n"
            f"🆔 ID: {uid}\n"
            f"🔗 Usuário: {username}\n"
            f"📌 Status: {info.get('status', 'Ainda não finalizou')}\n\n"
        )


    await update.message.reply_text(
        texto,
        reply_markup=teclado_professores()
    )



async def mostrar_reprovados(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not alunos_reprovados:

        await update.message.reply_text(
            "❌ Nenhum aluno reprovado ainda.",
            reply_markup=teclado_professores()
        )

        return


    keyboard = []

    for uid, info in alunos_reprovados.items():

        nome = info.get("nome", str(uid))

        keyboard.append([
            InlineKeyboardButton(
                f"❌ {nome}",
                callback_data=f"ver_reprovado_{uid}"
            )
        ])


    await update.message.reply_text(
        "❌ Alunos Reprovados\n\n"
        "Aqui ficam somente alunos reprovados.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # ================= LISTAS CONTINUAÇÃO =================

async def mostrar_entraram_oficial(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not alunos_no_oficial:

        await update.message.reply_text(
            "🏰 Nenhum aluno entrou no grupo oficial ainda.",
            reply_markup=teclado_professores()
        )

        return


    texto = (
        "🏰 Alunos que Entraram na Biblioteca de Hogwarts\n\n"
    )


    for uid, info in alunos_no_oficial.items():

        username = info.get(
            "username",
            "Sem usuário"
        )

        texto += (
            f"👤 Nome: {info.get('nome', 'Sem nome')}\n"
            f"🆔 ID: {uid}\n"
            f"🔗 Usuário: {username}\n"
            f"📌 Status: {info.get('status', 'Sem status')}\n\n"
        )


    await update.message.reply_text(
        texto,
        reply_markup=teclado_professores()
    )



async def mostrar_links_enviados(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not historico_links:

        await update.message.reply_text(
            "🔗 Nenhum link enviado ainda.",
            reply_markup=teclado_professores()
        )

        return


    texto = (
        f"🔗 Links Enviados\n\n"
        f"Total: {len(historico_links)}\n\n"
    )


    for uid, info in historico_links.items():

        texto += (
            f"👤 Nome: {info.get('nome', 'Sem nome')}\n"
            f"🆔 ID: {uid}\n"
            f"🔗 Usuário: @{info.get('username', 'Sem usuário')}\n"
            f"📌 Status: {info.get('status', 'Enviado')}\n\n"
        )


    await update.message.reply_text(
        texto,
        reply_markup=teclado_professores()
    )

# ================= TEXTO =================

async def receber_texto(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    texto = update.message.text.strip() if update.message.text else ""

    # ================= MENU DOS PROFESSORES =================

    if update.message.from_user.id == ADMIN_ID:

        # -------- MENU PRINCIPAL --------

        if texto == "📜 Fichas Aguardando":
            await mostrar_lista_fichas(update, context)
            return

        elif texto == "⚠️ Alunos Pendentes":
            await mostrar_pendentes(update, context)
            return

        elif texto == "✅ Alunos Aprovados":
            await mostrar_liberados(update, context)
            return

        elif texto == "❌ Alunos Reprovados":
            await mostrar_reprovados(update, context)
            return

        elif texto == "🧍 Entraram na Triagem":
            await mostrar_entradas_triagem(update, context)
            return

        elif texto == "🏰 Entraram no Oficial":
            await mostrar_entraram_oficial(update, context)
            return

        elif texto == "🔗 Links Enviados":
            await mostrar_links_enviados(update, context)
            return

        elif texto == "⚙️ Personalizar Acesso":

            context.user_data.pop("modo_admin", None)

            await update.message.reply_text(
                "⚙️ Personalização do acesso:\n\n"
                "Aqui você pode configurar exatamente como o acesso "
                "será enviado para os alunos aprovados.",
                reply_markup=teclado_personalizar()
            )
            return

        # -------- SUBMENU PERSONALIZAÇÃO --------

        elif texto == "🖼 Alterar imagem do acesso":

            context.user_data["modo_admin"] = "alterar_imagem_acesso"

            await update.message.reply_text(
                "🖼️ Alterar imagem do acesso\n\n"
                "Envie agora a imagem que deseja usar no acesso.\n\n"
                "📌 A imagem será enviada junto com a mensagem "
                "para todos os alunos aprovados.\n\n"
                "Se quiser remover a imagem atual, envie:\n"
                "remover"
            )
            return

        elif texto == "✏️ Alterar mensagem do acesso":

            context.user_data["modo_admin"] = "alterar_mensagem_acesso"

            await update.message.reply_text(
                "✏️ Alterar mensagem do acesso\n\n"
                "Envie agora o texto que deseja que o aluno receba "
                "quando for aprovado.\n\n"
                "💡 Você pode usar emojis e várias linhas."
            )
            return

        elif texto == "🔘 Alterar texto do botão":

            context.user_data["modo_admin"] = "alterar_botao_acesso"

            await update.message.reply_text(
                "🔘 Alterar texto do botão\n\n"
                "Envie agora o texto que aparecerá no botão "
                "de entrada da Biblioteca."
            )
            return

        elif texto == "👁 Visualizar acesso":

            context.user_data.pop("modo_admin", None)

            await enviar_preview_acesso(
                update,
                context
            )
            return

        elif texto == "🔙 Voltar":

            context.user_data.pop("modo_admin", None)

            await update.message.reply_text(
                "🏰✨ Voltamos para a Sala dos Professores.",
                reply_markup=teclado_professores()
            )
            return

    # ================= PERSONALIZAÇÃO =================

    if await processar_personalizacao_admin(update, context):
        return

    # ================= VERIFICAR =================

    if texto.lower() in ["verificar", "/verificar"]:
        await verificar_usuario(update, context)
        return

    # ================= TRIAGEM =================

    user_id = update.message.from_user.id
    user_key = k(user_id)

    if user_key not in usuarios:
        return

    etapa = usuarios[user_key]["etapa"]

    # ================= NOME =================

    if etapa == "nome":

        usuarios[user_key]["nome"] = texto
        usuarios[user_key]["etapa"] = "idade"

        alunos_entraram_triagem.setdefault(
            user_key,
            {
                "nome": texto,
                "username": update.message.from_user.username or "Sem usuário",
                "id": user_id,
                "status": "Respondendo triagem"
            }
        )

        alunos_entraram_triagem[user_key]["nome"] = texto
        alunos_entraram_triagem[user_key]["status"] = "Respondendo triagem"

        salvar_dados()

        await update.message.reply_text(
            "🎂 Agora diga sua idade:"
        )

    # ================= IDADE =================

    elif etapa == "idade":

        usuarios[user_key]["idade"] = texto
        usuarios[user_key]["etapa"] = "q1"

        alunos_entraram_triagem.setdefault(
            user_key,
            {
                "nome": usuarios[user_key].get(
                    "nome",
                    update.message.from_user.first_name
                ),
                "username": update.message.from_user.username or "Sem usuário",
                "id": user_id,
                "status": "Respondendo triagem"
            }
        )

        alunos_entraram_triagem[user_key]["status"] = "Respondendo triagem"

        salvar_dados()

        await perguntar(
            context,
            user_id,
            1
        )

# ================= BLOQUEAR MENU DO PROFESSOR =================

    if update.message.from_user.id == ADMIN_ID:

        comandos_professor = [
            "📜 Fichas Aguardando",
            "⚠️ Alunos Pendentes",
            "✅ Alunos Aprovados",
            "❌ Alunos Reprovados",
            "🧍 Entraram na Triagem",
            "🏰 Entraram no Oficial",
            "🔗 Links Enviados",
            "⚙️ Personalizar Acesso"
        ]

        if texto in comandos_professor:
            return


    # Personalização somente para o administrador
    if await processar_personalizacao_admin(update, context):
        return


    if texto.lower() in ["verificar", "/verificar"]:

        await verificar_usuario(update, context)

        return


    user_id = update.message.from_user.id
    user_key = k(user_id)


    if user_key not in usuarios:
        return


    etapa = usuarios[user_key]["etapa"]


    if etapa == "nome":

        usuarios[user_key]["nome"] = texto
        usuarios[user_key]["etapa"] = "idade"


        alunos_entraram_triagem.setdefault(
            user_key,
            {
                "nome": texto,
                "username": update.message.from_user.username or "Sem usuário",
                "id": user_id,
                "status": "Respondendo triagem"
            }
        )


        alunos_entraram_triagem[user_key]["nome"] = texto
        alunos_entraram_triagem[user_key]["status"] = "Respondendo triagem"


        salvar_dados()


        await update.message.reply_text(
            "🎂 Agora diga sua idade:"
        )



    elif etapa == "idade":

        usuarios[user_key]["idade"] = texto
        usuarios[user_key]["etapa"] = "q1"


        alunos_entraram_triagem.setdefault(
            user_key,
            {
                "nome": usuarios[user_key].get(
                    "nome",
                    update.message.from_user.first_name
                ),
                "username": update.message.from_user.username or "Sem usuário",
                "id": user_id,
                "status": "Respondendo triagem"
            }
        )


        alunos_entraram_triagem[user_key]["status"] = "Respondendo triagem"


        salvar_dados()


        await perguntar(
            context,
            user_id,
            1
        )



async def receber_midia(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # ================= PERSONALIZAÇÃO DA IMAGEM =================

    if update.message.from_user.id != ADMIN_ID:
        return

    modo = context.user_data.get("modo_admin")

    if modo != "alterar_imagem_acesso":
        return

    if not update.message.photo:
        return

    config_acesso["imagem_file_id"] = (
        update.message.photo[-1].file_id
    )

    salvar_dados()

    context.user_data.pop(
        "modo_admin",
        None
    )

    await update.message.reply_text(
        "✅🖼️ Imagem do acesso atualizada com sucesso!\n\n"
        "Essa será a imagem enviada aos alunos aprovados.",
        reply_markup=teclado_personalizar()
    )

    # ================= MENU DOS PROFESSORES =================

    if update.message.from_user.id == ADMIN_ID:

        if texto == "📜 Fichas Aguardando":
            await mostrar_lista_fichas(update, context)
            return

        elif texto == "⚠️ Alunos Pendentes":
            await mostrar_pendentes(update, context)
            return

        elif texto == "✅ Alunos Aprovados":
            await mostrar_liberados(update, context)
            return

        elif texto == "❌ Alunos Reprovados":
            await mostrar_reprovados(update, context)
            return

        elif texto == "🧍 Entraram na Triagem":
            await mostrar_entradas_triagem(update, context)
            return

        elif texto == "🏰 Entraram no Oficial":
            await mostrar_entraram_oficial(update, context)
            return

        elif texto == "🔗 Links Enviados":
            await mostrar_links_enviados(update, context)
            return

        elif texto == "⚙️ Personalizar Acesso":
            context.user_data.pop("modo_admin", None)

            await update.message.reply_text(
                "⚙️ Personalização do acesso:\n\n"
                "Aqui você pode configurar exatamente como o acesso "
                "será enviado para os alunos aprovados.",
                reply_markup=teclado_personalizar()
            )
            return

        elif texto == "🖼 Alterar imagem do acesso":
            context.user_data["modo_admin"] = "alterar_imagem_acesso"

            await update.message.reply_text(
                "🖼️ Alterar imagem do acesso\n\n"
                "Envie agora a imagem que deseja usar no acesso.\n\n"
                "📌 A imagem será enviada junto com a mensagem "
                "para todos os alunos aprovados.\n\n"
                "Se quiser remover a imagem atual, envie:\n"
                "remover",
                reply_markup=teclado_personalizar()
            )
            return

        elif texto == "✏️ Alterar mensagem do acesso":
            context.user_data["modo_admin"] = "alterar_mensagem_acesso"

            await update.message.reply_text(
                "✏️ Alterar mensagem do acesso\n\n"
                "Envie agora o texto que deseja que o aluno receba "
                "quando for aprovado.\n\n"
                "💡 Você pode usar emojis e várias linhas.",
                reply_markup=teclado_personalizar()
            )
            return

        elif texto == "🔘 Alterar texto do botão":
            context.user_data["modo_admin"] = "alterar_botao_acesso"

            await update.message.reply_text(
                "🔘 Alterar texto do botão\n\n"
                "Envie agora o texto que aparecerá no botão "
                "de entrada da Biblioteca.",
                reply_markup=teclado_personalizar()
            )    
            return

        elif texto == "👁 Visualizar acesso":
            context.user_data.pop("modo_admin", None)

            await enviar_preview_acesso(
                update,
                context
            )

            return

        elif texto == "🔙 Voltar":
            context.user_data.pop("modo_admin", None)

            await update.message.reply_text(
                "🏰✨ Voltamos para a Sala dos Professores.",
                reply_markup=teclado_professores()
            )
            return

    # ================= PERGUNTAR =================

async def perguntar(
    context: ContextTypes.DEFAULT_TYPE,
    user_id,
    num
):

    # Pega a pergunta atual
    pergunta_atual = perguntas[num - 1]

    # Pega o texto da pergunta
    texto_pergunta = pergunta_atual["pergunta"]

    # Cria os botões com as opções da pergunta
    keyboard = []

    for indice, opcao in enumerate(pergunta_atual["opcoes"]):
        keyboard.append([
            InlineKeyboardButton(
                opcao,
                callback_data=f"{num}_opcao_{indice}"
            )
        ])

    await context.bot.send_message(
        chat_id=user_id,
        text=(
            f"📚 {num}/{len(perguntas)}\n\n"
            f"{texto_pergunta}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ================= RESPOSTAS DA TRIAGEM =================

async def responder(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    user_key = k(user_id)

    # Verifica se a triagem está ativa
    if user_key not in usuarios:

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"{NOME_GUARDIA}\n\n"
                "⚠️ Esta Triagem Literária não está ativa para você.\n\n"
                "🏰 Entre primeiro no grupo Expresso Hogwarts "
                "e utilize o botão oficial enviado pela Coruja "
                "da Biblioteca para iniciar sua triagem."
            )
        )

        return

    data = query.data

    # Esperado:
    # 1_opcao_0
    # 1_opcao_1
    # 2_opcao_3
    # etc.

    try:
        partes = data.split("_")

        num = int(partes[0])
        indice_opcao = int(partes[2])

    except (ValueError, IndexError):
        return

    # Verifica se a pergunta existe
    if num < 1 or num > len(perguntas):
        return

    pergunta_atual = perguntas[num - 1]

    opcoes = pergunta_atual.get("opcoes", [])

    # Verifica se a opção existe
    if indice_opcao < 0 or indice_opcao >= len(opcoes):
        return

    resposta = opcoes[indice_opcao]

    # ================= SALVAR RESPOSTA =================

    usuarios[user_key][f"q{num}"] = resposta

    # Também guardamos a pergunta e resposta organizadas
    if "respostas" not in usuarios[user_key]:
        usuarios[user_key]["respostas"] = {}

    usuarios[user_key]["respostas"][str(num)] = {
        "pergunta": pergunta_atual["pergunta"],
        "resposta": resposta
    }

    # Atualiza etapa
    usuarios[user_key]["etapa"] = f"q{num}"

    # Atualiza status
    if user_key in alunos_entraram_triagem:

        alunos_entraram_triagem[user_key]["status"] = (
            f"Respondendo triagem "
            f"({num}/{len(perguntas)})"
        )

    salvar_dados()

    # Remove os botões da pergunta respondida
    try:
        await query.edit_message_reply_markup(
            reply_markup=None
        )
    except Exception:
        pass

    # ================= PRÓXIMA PERGUNTA =================

    proxima = num + 1

    if proxima <= len(perguntas):

        await perguntar(
            context,
            user_id,
            proxima
        )

    else:

        await finalizar(
            context,
            user_id
        )

# ================= FICHA =================

async def montar_ficha(
    user_id,
    context=None
):

    user_key = k(user_id)

    dados = usuarios.get(
        user_key,
        {}
    )

    nome = dados.get(
        "nome",
        "Não informado"
    )

    idade = dados.get(
        "idade",
        "Não informado"
    )

    perfil_extra = (
        await texto_perfil(
            context,
            user_id
        )
        if context
        else
        f"🆔 ID Telegram: {user_id}\n"
    )

    texto = (
        f"{NOME_GUARDIA}\n\n"
        "🧪 FICHA DE ALUNO\n\n"
        f"👤 Nome: {nome}\n"
        f"🎂 Idade: {idade}\n"
        f"{perfil_extra}"
        "📌 Status: aguardando avaliação\n"
    )

    for i in range(1, len(perguntas) + 1):

        pergunta_atual = perguntas[i - 1]

        texto += (
            f"\n{i}. {pergunta_atual['pergunta']}\n"
            f"Resposta: {dados.get(f'q{i}', 'Não respondeu')}\n"
        )

    return texto

async def finalizar(
    context: ContextTypes.DEFAULT_TYPE,
    user_id
):

    user_key = k(user_id)

    texto = await montar_ficha(
        user_id,
        context
    )


    tem_foto, tem_usuario, username = await verificar_perfil(
        context,
        user_id
    )


    if not tem_foto or not tem_usuario:

        motivos = []


        if not tem_foto:
            motivos.append(
                "• Colocar uma imagem/foto no perfil"
            )


        if not tem_usuario:
            motivos.append(
                "• Criar ou atualizar seu usuário do Telegram, exemplo: @seunome"
            )


        nome = usuarios.get(
            user_key,
            {}
        ).get(
            "nome",
            str(user_id)
        )


        alunos_pendentes[user_key] = {
            "nome": nome,
            "motivos": motivos,
            "ficha": texto,
            "status": "Finalizou a triagem, mas precisa corrigir perfil antes da avaliação"
        }


        fichas_alunos.pop(
            user_key,
            None
        )


        if user_key in alunos_entraram_triagem:

            alunos_entraram_triagem[user_key]["status"] = (
                "Finalizou triagem, mas ficou pendente de perfil"
            )


        salvar_dados()


        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                f"{NOME_GUARDIA}\n\n"
                "⚠️ Uma ficha foi finalizada, mas o aluno ficou em Pendentes por falta de foto/usuário.\n\n"
                f"👤 Nome: {nome}\n"
                f"🆔 ID: {user_id}\n\n"
                "Pendências:\n"
                + "\n".join(motivos)
            )
        )


        await context.bot.send_message(
            chat_id=user_id,
            text=(
                f"{NOME_GUARDIA}\n\n"
                "⚠️ Sua Triagem Literária foi finalizada, mas antes da avaliação você precisa organizar seu perfil:\n\n"
                + "\n".join(motivos)
                +
                "\n\nAssim que atualizar, volte aqui no PV da Coruja da Biblioteca e envie:\n\n"
                "/verificar\n\n"
                "Se não conseguir alterar esses detalhes, mande mensagem no grupo de triagem para que um dos professores/administradores possa te ajudar. ✨"
            )
        )

        return

    # Fichas dos alunos = somente aguardando aprovação
    fichas_alunos[user_key] = texto

    if user_key in alunos_entraram_triagem:
        alunos_entraram_triagem[user_key]["status"] = "Finalizou triagem, aguardando avaliação"

    salvar_dados()

    keyboard = [[
        InlineKeyboardButton("📜 Abrir Fichas Aguardando", callback_data="menu_fichas")
    ]]

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"{NOME_GUARDIA}\n\n"
            "📜 Uma nova ficha de aluno foi registrada.\n\n"
            "Ela está em: 📜 Fichas Aguardando."
        ),
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    await context.bot.send_message(
        chat_id=user_id,
        text=(
            "🔮✨ Sua Triagem Literária foi enviada para análise.\n\n"
            "Aguarde a resposta dos professores."
        )
    )

# ================= PERFIL / LINK =================
async def verificar_perfil(context, user_id):

    chat = await context.bot.get_chat(user_id)

    username = chat.username

    fotos = await context.bot.get_user_profile_photos(
        user_id,
        limit=1
    )

    tem_foto = fotos.total_count > 0

    tem_usuario = (
        username is not None
        and username.strip() != ""
    )

    return tem_foto, tem_usuario, username


async def criar_link_unico(context, user_id):
    """Cria um convite exclusivo para o ID aprovado.

    O Telegram não prende o URL a um usuário por conta própria; a trava real
    é feita em processar_solicitacao_entrada, comparando o ID e o link usado.
    """
    user_key = k(user_id)

    # Se existir convite anterior ainda registrado para este ID, revoga antes
    # de criar outro. Assim cada aluno mantém somente um acesso ativo.
    registro_anterior = links_enviados.get(user_key)
    if registro_anterior:
        link_anterior = registro_anterior.get("invite_link")
        if link_anterior:
            try:
                await context.bot.revoke_chat_invite_link(
                    chat_id=GRUPO_OFICIAL_ID,
                    invite_link=link_anterior
                )
            except Exception as erro:
                print(f"⚠️ Não foi possível revogar convite anterior de {user_id}: {erro}")

    convite = await context.bot.create_chat_invite_link(
        chat_id=GRUPO_OFICIAL_ID,
        creates_join_request=True,
        name=f"acesso_{user_id}"
    )

    return convite.invite_link

# ================= ENVIAR LINK INDIVIDUAL =================

async def enviar_link_unico(
    context,
    user_id,
    nome,
    username
):

    user_key = k(user_id)

    # Cria um convite que exige solicitação de entrada
    link = await criar_link_unico(context, user_id)

    keyboard = [[
        InlineKeyboardButton(
            config_acesso["texto_botao"],
            url=link
        )
    ]]

    texto = (
        f"{NOME_GUARDIA}\n\n"
        f"{config_acesso['mensagem']}"
    )

    # Envia o acesso para o aluno
    if config_acesso.get("imagem_file_id"):

        msg = await context.bot.send_photo(
            chat_id=user_id,
            photo=config_acesso["imagem_file_id"],
            caption=texto,
            reply_markup=InlineKeyboardMarkup(keyboard),
            protect_content=True
        )

    else:

        msg = await context.bot.send_message(
            chat_id=user_id,
            text=texto,
            reply_markup=InlineKeyboardMarkup(keyboard),
            protect_content=True
        )

    # ================= REGISTRAR LINK =================

    links_enviados[user_key] = {
        "message_id": msg.message_id,
        "invite_link": link
    }

    historico_links[user_key] = {
        "nome": nome,
        "username": username,
        "invite_link": link,
        "status": "Convite individual enviado"
    }

    salvar_dados()

# ================= SOLICITAÇÃO DE ENTRADA =================

async def processar_solicitacao_entrada(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    request = update.chat_join_request

    user_id = request.from_user.id
    user_key = k(user_id)

    print(
        f"🔐 Solicitação de entrada recebida: "
        f"{user_id}"
    )

    # Só aceita solicitações do grupo oficial
    if request.chat.id != GRUPO_OFICIAL_ID:
        return

    # ================= VERIFICAR APROVAÇÃO =================

    if user_key not in alunos_liberados:

        print(
            f"❌ Entrada recusada: "
            f"{user_id} não está liberado."
        )

        try:
            await context.bot.decline_chat_join_request(
                chat_id=GRUPO_OFICIAL_ID,
                user_id=user_id
            )
        except Exception as erro:
            print(
                f"Erro ao recusar solicitação: {erro}"
            )

        return

    # ================= VERIFICAR LINK =================

    registro_link = links_enviados.get(user_key)

    if not registro_link:

        print(
            f"❌ Entrada recusada: "
            f"nenhum link registrado para {user_id}."
        )

        try:
            await context.bot.decline_chat_join_request(
                chat_id=GRUPO_OFICIAL_ID,
                user_id=user_id
            )
        except Exception as erro:
            print(
                f"Erro ao recusar solicitação: {erro}"
            )

        return

    invite_link_usado = (
        request.invite_link.invite_link
        if request.invite_link
        else None
    )

    invite_link_autorizado = registro_link.get(
        "invite_link"
    )

    # ================= COMPARAR LINK =================

    if invite_link_usado != invite_link_autorizado:

        print(
            f"❌ Entrada recusada: link inválido "
            f"para {user_id}."
        )

        try:
            await context.bot.decline_chat_join_request(
                chat_id=GRUPO_OFICIAL_ID,
                user_id=user_id
            )
        except Exception as erro:
            print(
                f"Erro ao recusar solicitação: {erro}"
            )

        return

    # ================= CONSUMIR O CONVITE =================

    # O ID correto chegou usando o link correto. Revogamos imediatamente,
    # antes da aprovação, para que o mesmo URL não gere novas solicitações.
    try:
        await context.bot.revoke_chat_invite_link(
            chat_id=GRUPO_OFICIAL_ID,
            invite_link=invite_link_autorizado
        )
        print(f"🔒 Convite consumido/revogado para {user_id}")
    except Exception as erro:
        print(f"❌ Não foi possível consumir o convite de {user_id}: {erro}")
        try:
            await context.bot.decline_chat_join_request(
                chat_id=GRUPO_OFICIAL_ID,
                user_id=user_id
            )
        except Exception:
            pass
        return

    # ================= AUTORIZAÇÃO FINAL =================

    try:

        await context.bot.approve_chat_join_request(
            chat_id=GRUPO_OFICIAL_ID,
            user_id=user_id
        )

        print(
            f"✅ Entrada aprovada automaticamente: "
            f"{user_id}"
        )

    except Exception as erro:

        print(
            f"❌ Erro ao aprovar {user_id}: {erro}"
        )

        return

    # ================= ATUALIZAR STATUS =================

    if user_key in alunos_liberados:

        alunos_liberados[user_key]["status"] = (
            "Entrou no grupo oficial"
        )

    if user_key in historico_links:

        historico_links[user_key]["status"] = (
            "Utilizado e entrou no grupo oficial"
        )

    alunos_no_oficial[user_key] = {
        "nome": request.from_user.first_name,
        "username": request.from_user.username or "Sem usuário",
        "id": user_id,
        "status": "Entrou após aprovação automática"
    }

    salvar_dados()

    # ================= APAGAR MENSAGEM DO LINK =================

    try:

        message_id = registro_link.get(
            "message_id"
        )

        if message_id:

            await context.bot.delete_message(
                chat_id=user_id,
                message_id=message_id
            )

            print(
                f"🗑️ Mensagem do convite apagada "
                f"para {user_id}"
            )

    except Exception as erro:

        print(
            f"⚠️ Não foi possível apagar "
            f"a mensagem do convite: {erro}"
        )

    # ================= REMOVER REGISTRO =================

    links_enviados.pop(
        user_key,
        None
    )

    salvar_dados()
# ================= COMANDO VERIFICAR =================
async def verificar_usuario(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.message.from_user.id
    user_key = k(user_id)

    nome = usuarios.get(
        user_key,
        {}
    ).get(
        "nome",
        update.message.from_user.first_name
    )

    if user_key not in alunos_pendentes and user_key not in alunos_liberados:

        await update.message.reply_text(
            f"{NOME_GUARDIA}\n\n"
            "📜 Ainda não encontrei uma aprovação para você.\n\n"
            "Primeiro faça a Triagem Literária e aguarde a avaliação dos professores."
        )
        return

    tem_foto, tem_usuario, username = await verificar_perfil(context, user_id)

    if tem_foto and tem_usuario:
        await enviar_link_unico(
            context,
            user_id,
            nome,
            username
        )

        if user_key in alunos_pendentes:
            ficha = alunos_pendentes[user_key].get("ficha", ficha_do_aluno(user_key))
            alunos_pendentes.pop(user_key, None)
            alunos_liberados[user_key] = {
                "nome": nome,
                "username": username,
                "status": "Perfil corrigido, link enviado",
                "ficha": ficha
            }
            salvar_dados()

        await context.bot.send_message(
            chat_id=GRUPO_TRIAGEM_ID,
            text=(
                "✨📜 Um aluno organizou seu perfil e foi liberado para a Biblioteca de Hogwarts! 🏰📖"
            )
        )
    else:
        pendencias = []

        if not tem_foto:
            pendencias.append("• Colocar uma imagem/foto no perfil")

        if not tem_usuario:
            pendencias.append("• Criar ou atualizar seu usuário do Telegram, exemplo: @seunome")

        alunos_pendentes[user_key] = {
            "nome": nome,
            "username": username or "Sem usuário",
            "motivos": pendencias,
            "ficha": ficha_do_aluno(user_key),
            "status": "Ainda precisa corrigir perfil"
        }
        salvar_dados()

        await update.message.reply_text(
            f"{NOME_GUARDIA}\n\n"
            "⚠️ Ainda não conseguimos finalizar sua inscrição.\n\n"
            "Para entrar no grupo oficial Biblioteca de Hogwarts 🏰📖, organize estes detalhes:\n\n"
            + "\n".join(pendencias) +
            "\n\nAssim que atualizar, volte aqui no PV da Coruja da Biblioteca e envie:\n\n"
            "/verificar\n\n"
            "Se não conseguir alterar esses detalhes, mande mensagem no grupo de triagem "
            "para que um dos professores/administradores possa te ajudar. ✨"
        )

# ================= DECISÃO =================
async def decisao(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    acao, user_id = query.data.split("_")
    user_id = int(user_id)
    user_key = k(user_id)

    nome = usuarios.get(user_key, {}).get("nome", str(user_id))
    ficha = ficha_do_aluno(user_key)

    if acao == "aprovar":
        tem_foto, tem_usuario, username = await verificar_perfil(context, user_id)

        # Sai de Fichas Aguardando
        fichas_alunos.pop(user_key, None)

        if not tem_foto or not tem_usuario:
            motivos = []

            if not tem_foto:
                motivos.append("• Colocar uma imagem/foto no perfil")

            if not tem_usuario:
                motivos.append("• Criar ou atualizar seu usuário do Telegram, exemplo: @seunome")

            alunos_pendentes[user_key] = {
                "nome": nome,
                "username": username or "Sem usuário",
                "motivos": motivos,
                "ficha": ficha,
                "status": "Aprovado, mas pendente de perfil"
            }

            salvar_dados()

            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    f"{NOME_GUARDIA}\n\n"
                    "🦉📜 Sua ficha foi aprovada pelos professores!\n\n"
                    "Mas para finalizar sua inscrição e receber o acesso à Biblioteca de Hogwarts 🏰📖, "
                    "você precisa atualizar seu perfil:\n\n"
                    + "\n".join(motivos) +
                    "\n\nAssim que atualizar esses detalhes, volte aqui no PV da Coruja da Biblioteca e envie:\n\n"
                    "/verificar\n\n"
                    "A Coruja vai conferir novamente e, se estiver tudo certo, enviará o convite único do grupo oficial.\n\n"
                    "Se você não conseguir trocar esses detalhes, mande mensagem no grupo de triagem "
                    "para que um dos professores/administradores possa te ajudar. ✨"
                )
            )

            await query.edit_message_reply_markup(
                reply_markup=None
            )
            await query.message.reply_text("⚠️ Aluno movido para Alunos Pendentes.")
            return

        alunos_liberados[user_key] = {
            "nome": nome,
            "username": username,
            "status": "Aprovado, link enviado",
            "ficha": ficha
        }

        salvar_dados()
        await enviar_link_unico(
            context,
            user_id,
            nome,
            username
        )

        await context.bot.send_message(
            chat_id=GRUPO_TRIAGEM_ID,
            text=(
                "✨📜 Um novo aluno foi aprovado pelos professores!\n\n"
                "🏰📖 A Biblioteca de Hogwarts acaba de receber mais um membro."
            )
        )

        await query.edit_message_reply_markup(
            reply_markup=None
        )
        await query.message.reply_text(("✅ Aluno movido para Aprovados e convite único enviado.")
        )
    else:
        # Sai de Fichas Aguardando
        fichas_alunos.pop(user_key, None)

        alunos_reprovados[user_key] = {
            "nome": nome,
            "status": "Reprovado",
            "ficha": ficha
        }

        salvar_dados()

        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ Sua entrada não foi aprovada no momento.\n\n"
                "Agradecemos por responder a Triagem Literária."
            )
        )

        await query.edit_message_reply_markup(
            reply_markup=None
        )
        await query.message.reply_text(
            "❌ Aluno movido para Reprovados."
        )

# ================= CALLBACK MENUS =================
async def menu_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        return

    data = query.data

    if data == "menu_fichas":

        if not fichas_alunos:

            await query.message.reply_text(
                "📜 Nenhuma ficha aguardando avaliação."
            )

            return

        keyboard = []
        for uid in fichas_alunos:
            nome = usuarios.get(uid, {}).get("nome", str(uid))
            keyboard.append([InlineKeyboardButton(f"👤 {nome}", callback_data=f"ver_ficha_{uid}")])

        await query.message.reply_text("📜 Fichas Aguardando:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif data.startswith("ver_ficha_"):
        uid = data.replace("ver_ficha_", "")
        ficha = fichas_alunos.get(uid, "Ficha não encontrada.")

        keyboard = [[
            InlineKeyboardButton("✅ Aprovar", callback_data=f"aprovar_{uid}"),
            InlineKeyboardButton("❌ Reprovar", callback_data=f"reprovar_{uid}")
        ]]

        await query.message.reply_text(
            ficha,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("ver_aprovado_"):
        uid = data.replace("ver_aprovado_", "")
        await query.message.reply_text(
            alunos_liberados.get(uid, {}).get("ficha", "Ficha não encontrada.")
        )

    elif data.startswith("ver_reprovado_"):
        uid = data.replace("ver_reprovado_", "")
        await query.message.reply_text(
            alunos_reprovados.get(uid, {}).get("ficha", "Ficha não encontrada.")
        )

    elif data.startswith("ver_pendente_"):
        uid = data.replace("ver_pendente_", "")
        item = alunos_pendentes.get(uid)

        if not item:
            await query.message.reply_text("Esse aluno não está mais pendente.")
            return

        motivos = "\n".join(item["motivos"])

        username = item.get("username") or usuarios.get(uid, {}).get("username") or "Sem usuário"
        if username != "Sem usuário" and not str(username).startswith("@"):
            username = "@" + str(username)

        perfil = f"tg://user?id={uid}"

        keyboard = [
            [InlineKeyboardButton("🔄 Verificar novamente", callback_data=f"reverificar_{uid}")],
            [InlineKeyboardButton("✅ Liberar mesmo com pendência", callback_data=f"liberar_forcado_{uid}")]
        ]

        await query.message.reply_text(
            f"⚠️ Aluno Pendente\n\n"
            f"👤 {item.get('nome', uid)}\n"
            f"🆔 ID: {uid}\n"
            f"🔗 Usuário: {username}\n"
            f"👁 Perfil: {perfil}\n\n"
            f"Pendências:\n{motivos}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data.startswith("liberar_forcado_"):
        uid = data.replace("liberar_forcado_", "")
        nome = usuarios.get(uid, {}).get("nome", alunos_pendentes.get(uid, {}).get("nome", str(uid)))

        try:
            chat = await context.bot.get_chat(int(uid))
            username = chat.username or "Sem usuário"
        except Exception:
            username = "Sem usuário"

        ficha = alunos_pendentes.get(uid, {}).get("ficha", ficha_do_aluno(uid))

        alunos_pendentes.pop(uid, None)
        alunos_liberados[uid] = {
            "nome": nome,
            "username": username,
            "status": "Liberado manualmente pela professora, mesmo com pendência",
            "ficha": ficha
        }
        salvar_dados()

        await enviar_link_unico(
            context,
            int(uid),
            nome,
            username
        )

        await query.message.reply_text(
            "✅ Aluno liberado manualmente.\n\n"
            "A Coruja enviou o convite único no PV do aluno."
        )

    elif data.startswith("reverificar_"):
        uid = data.replace("reverificar_", "")
        nome = usuarios.get(uid, {}).get("nome", str(uid))

        tem_foto, tem_usuario, username = await verificar_perfil(
            context,
            int(uid)
        )

        if tem_foto and tem_usuario:
            ficha = alunos_pendentes.get(uid, {}).get("ficha", ficha_do_aluno(uid))
            alunos_pendentes.pop(uid, None)
            alunos_liberados[uid] = {
                "nome": nome,
                "username": username,
                "status": "Perfil corrigido, link enviado",
                "ficha": ficha
            }
            salvar_dados()
            await enviar_link_unico(
                context,
                int(uid),
                nome,
                username
            )
            await query.message.reply_text("✅ Perfil corrigido. Aluno movido para Aprovados e convite único enviado.")
        else:
            motivos = []

            if not tem_foto:
                motivos.append("• Ainda falta foto/imagem no perfil")

            if not tem_usuario:
                motivos.append("• Ainda falta usuário @ no Telegram")

            alunos_pendentes[uid]["motivos"] = motivos
            salvar_dados()

            await query.message.reply_text(
                "⚠️ O perfil ainda não está completo:\n\n"
                + "\n".join(motivos)
            )

# ================= COMANDO VERIFICAR =================

    user_id = update.message.from_user.id

    user_key = k(user_id)

    nome = usuarios.get(
        user_key,
        {}
    ).get(
        "nome",
        update.message.from_user.first_name
    )


    if (
        user_key not in alunos_pendentes
        and user_key not in alunos_liberados
    ):

        await update.message.reply_text(
            f"{NOME_GUARDIA}\n\n"
            "📜 Ainda não encontrei uma aprovação para você.\n\n"
            "Primeiro faça a Triagem Literária e aguarde a avaliação dos professores."
        )

        return



    tem_foto, tem_usuario, username = await verificar_perfil(
        context,
        user_id
    )


    if tem_foto and tem_usuario:


        await enviar_link_unico(
            context,
            user_id,
            nome,
            username
        )


        if user_key in alunos_pendentes:

            ficha = alunos_pendentes[user_key].get(
                "ficha",
                ficha_do_aluno(user_key)
            )


            alunos_pendentes.pop(
                user_key,
                None
            )


            alunos_liberados[user_key] = {
                "nome": nome,
                "username": username,
                "status": "Perfil corrigido, link enviado",
                "ficha": ficha
            }


            salvar_dados()



        await context.bot.send_message(
            chat_id=GRUPO_TRIAGEM_ID,
            text=(
                "✨📜 Um aluno organizou seu perfil e foi liberado "
                "para a Biblioteca de Hogwarts! 🏰📖"
            )
        )



    else:

        pendencias = []


        if not tem_foto:

            pendencias.append(
                "• Colocar uma imagem/foto no perfil"
            )


        if not tem_usuario:

            pendencias.append(
                "• Criar ou atualizar seu usuário do Telegram, exemplo: @seunome"
            )


        alunos_pendentes[user_key] = {

            "nome": nome,

            "username": username or "Sem usuário",

            "motivos": pendencias,

            "ficha": ficha_do_aluno(user_key),

            "status": "Ainda precisa corrigir perfil"
        }


        salvar_dados()



        await update.message.reply_text(
            f"{NOME_GUARDIA}\n\n"
            "⚠️ Ainda não conseguimos finalizar sua inscrição.\n\n"
            "Para entrar no grupo oficial Biblioteca de Hogwarts 🏰📖, "
            "organize estes detalhes:\n\n"
            + "\n".join(pendencias)
            +
            "\n\nAssim que atualizar, volte aqui no PV da Coruja da Biblioteca e envie:\n\n"
            "/verificar\n\n"
            "Se não conseguir alterar esses detalhes, mande mensagem no grupo de triagem "
            "para que um dos professores/administradores possa te ajudar. ✨"
        )

# ================= DECISÃO =================

    query = update.callback_query

    await query.answer()


    acao, user_id = query.data.split("_")

    user_id = int(user_id)

    user_key = k(user_id)


    nome = usuarios.get(
        user_key,
        {}
    ).get(
        "nome",
        str(user_id)
    )


    ficha = ficha_do_aluno(user_key)



    if acao == "aprovar":


        tem_foto, tem_usuario, username = await verificar_perfil(
            context,
            user_id
        )


        # Sai de Fichas Aguardando
        fichas_alunos.pop(
            user_key,
            None
        )



        if not tem_foto or not tem_usuario:

            motivos = []


            if not tem_foto:
                motivos.append(
                    "• Colocar uma imagem/foto no perfil"
                )


            if not tem_usuario:
                motivos.append(
                    "• Criar ou atualizar seu usuário do Telegram, exemplo: @seunome"
                )



            alunos_pendentes[user_key] = {

                "nome": nome,

                "username": username or "Sem usuário",

                "motivos": motivos,

                "ficha": ficha,

                "status": "Aprovado, mas pendente de perfil"
            }


            salvar_dados()



            await context.bot.send_message(
                chat_id=user_id,
                text=(
                    f"{NOME_GUARDIA}\n\n"
                    "🦉📜 Sua ficha foi aprovada pelos professores!\n\n"
                    "Mas para finalizar sua inscrição e receber o acesso à Biblioteca de Hogwarts 🏰📖, "
                    "você precisa atualizar seu perfil:\n\n"
                    + "\n".join(motivos)
                    +
                    "\n\nAssim que atualizar esses detalhes, volte aqui no PV da Coruja da Biblioteca e envie:\n\n"
                    "/verificar\n\n"
                    "A Coruja vai conferir novamente e, se estiver tudo certo, enviará o convite único do grupo oficial.\n\n"
                    "Se você não conseguir trocar esses detalhes, mande mensagem no grupo de triagem "
                    "para que um dos professores/administradores possa te ajudar. ✨"
                )
            )


            await query.edit_message_reply_markup(
                reply_markup=None
            )


            await query.message.reply_text(
                "⚠️ Aluno movido para Alunos Pendentes."
            )

            return



        alunos_liberados[user_key] = {

            "nome": nome,

            "username": username,

            "status": "Aprovado, link enviado",

            "ficha": ficha
        }



        salvar_dados()



        await enviar_link_unico(
            context,
            user_id,
            nome,
            username
        )



        await context.bot.send_message(
            chat_id=GRUPO_TRIAGEM_ID,
            text=(
                "✨📜 Um novo aluno foi aprovado pelos professores!\n\n"
                "🏰📖 A Biblioteca de Hogwarts acaba de receber mais um membro."
            )
        )



        await query.edit_message_reply_markup(
            reply_markup=None
        )


        await query.message.reply_text(
            "✅ Aluno movido para Aprovados e convite único enviado."
        )



    else:


        # Sai de Fichas Aguardando
        fichas_alunos.pop(
            user_key,
            None
        )


        alunos_reprovados[user_key] = {

            "nome": nome,

            "status": "Reprovado",

            "ficha": ficha
        }



        salvar_dados()



        await context.bot.send_message(
            chat_id=user_id,
            text=(
                "❌ Sua entrada não foi aprovada no momento.\n\n"
                "Agradecemos por responder a Triagem Literária."
            )
        )



        await query.edit_message_reply_markup(
            reply_markup=None
        )


        await query.message.reply_text(
            "❌ Aluno movido para Reprovados."
        )

# ================= CALLBACK MENUS =================
    
    query = update.callback_query

    await query.answer()


    if query.from_user.id != ADMIN_ID:
        return


    data = query.data



    if data == "menu_fichas":

        if not fichas_alunos:

            await query.message.reply_text(
                "📜 Nenhuma ficha aguardando avaliação."
            )

            return


        keyboard = []


        for uid in fichas_alunos:

            nome = usuarios.get(
                uid,
                {}
            ).get(
                "nome",
                str(uid)
            )


            keyboard.append([
                InlineKeyboardButton(
                    f"👤 {nome}",
                    callback_data=f"ver_ficha_{uid}"
                )
            ])


        await query.message.reply_text(
            "📜 Fichas Aguardando:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



    elif data.startswith("ver_ficha_"):

        uid = data.replace(
            "ver_ficha_",
            ""
        )


        ficha = fichas_alunos.get(
            uid,
            "Ficha não encontrada."
        )


        keyboard = [[

            InlineKeyboardButton(
                "✅ Aprovar",
                callback_data=f"aprovar_{uid}"
            ),

            InlineKeyboardButton(
                "❌ Reprovar",
                callback_data=f"reprovar_{uid}"
            )

        ]]


        await query.message.reply_text(
            ficha,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



    elif data.startswith("ver_aprovado_"):

        uid = data.replace(
            "ver_aprovado_",
            ""
        )


        await query.message.reply_text(
            alunos_liberados.get(
                uid,
                {}
            ).get(
                "ficha",
                "Ficha não encontrada."
            )
        )



    elif data.startswith("ver_reprovado_"):

        uid = data.replace(
            "ver_reprovado_",
            ""
        )


        await query.message.reply_text(
            alunos_reprovados.get(
                uid,
                {}
            ).get(
                "ficha",
                "Ficha não encontrada."
            )
        )



    elif data.startswith("ver_pendente_"):

        uid = data.replace(
            "ver_pendente_",
            ""
        )


        item = alunos_pendentes.get(uid)


        if not item:

            await query.message.reply_text(
                "Esse aluno não está mais pendente."
            )

            return



        motivos = "\n".join(
            item["motivos"]
        )


        username = (
            item.get("username")
            or usuarios.get(uid, {}).get("username")
            or "Sem usuário"
        )


        if (
            username != "Sem usuário"
            and not str(username).startswith("@")
        ):
            username = "@" + str(username)


        perfil = f"tg://user?id={uid}"


        keyboard = [

            [
                InlineKeyboardButton(
                    "🔄 Verificar novamente",
                    callback_data=f"reverificar_{uid}"
                )
            ],

            [
                InlineKeyboardButton(
                    "✅ Liberar mesmo com pendência",
                    callback_data=f"liberar_forcado_{uid}"
                )
            ]

        ]


        await query.message.reply_text(

            f"⚠️ Aluno Pendente\n\n"
            f"👤 {item.get('nome', uid)}\n"
            f"🆔 ID: {uid}\n"
            f"🔗 Usuário: {username}\n"
            f"👁 Perfil: {perfil}\n\n"
            f"Pendências:\n{motivos}",

            reply_markup=InlineKeyboardMarkup(keyboard)
        )



    elif data.startswith("liberar_forcado_"):

        uid = data.replace(
            "liberar_forcado_",
            ""
        )


        nome = usuarios.get(
            uid,
            {}
        ).get(
            "nome",
            alunos_pendentes.get(uid, {}).get(
                "nome",
                str(uid)
            )
        )


        try:

            chat = await context.bot.get_chat(
                int(uid)
            )

            username = chat.username or "Sem usuário"


        except Exception:

            username = "Sem usuário"



        ficha = alunos_pendentes.get(
            uid,
            {}
        ).get(
            "ficha",
            ficha_do_aluno(uid)
        )


        alunos_pendentes.pop(
            uid,
            None
        )


        alunos_liberados[uid] = {

            "nome": nome,

            "username": username,

            "status": "Liberado manualmente pela professora, mesmo com pendência",

            "ficha": ficha

        }


        salvar_dados()



        await enviar_link_unico(
            context,
            int(uid),
            nome,
            username
        )


        await query.message.reply_text(
            "✅ Aluno liberado manualmente.\n\n"
            "A Coruja enviou o convite único no PV do aluno."
        )


# ================= MAIN =================

def main():

    carregar_dados()

    application = Application.builder().token(TOKEN).build()


    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "verificar",
            verificar_usuario
        )
    )

    application.add_handler(
        MessageHandler(
            filters.StatusUpdate.NEW_CHAT_MEMBERS,
            novo_membro
        )
    )

    application.add_handler(
        ChatJoinRequestHandler(
            processar_solicitacao_entrada
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            receber_texto
        )
    )

    application.add_handler(
        MessageHandler(
            filters.PHOTO,
            receber_midia
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            menu_callback,
            pattern=(
                r"menu_|"
                r"ver_ficha_|"
                r"ver_pendente_|"
                r"reverificar_|"
                r"liberar_forcado_|"
                r"ver_aprovado_|"
                r"ver_reprovado_|"
                r"personalizar_"
            )
        )
    )

    application.add_handler(
    CallbackQueryHandler(
        responder,
        pattern=r"^\d+_opcao_\d+$"
    )
)

    application.add_handler(
        CallbackQueryHandler(
            decisao,
            pattern=r"(aprovar|reprovar)_"
        )
    )

    print(
        "🦉 Coruja da Biblioteca rodando com fichas organizadas por setor..."
    )

    application.run_polling(
        allowed_updates=[
            "message",
            "callback_query",
            "chat_member",
            "chat_join_request"
        ]
    )

if __name__ == "__main__":
    main()
