<div align="center">

# 🎓 Помощник студента

**Telegram-бот с расписанием и домашними заданиями для твоей группы**

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-3.x-2CA5E0?logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-база-003B57?logo=sqlite&logoColor=white)
![Amvera](https://img.shields.io/badge/хостинг-Amvera-FF6B35)
![Статус](https://img.shields.io/badge/статус-в_разработке-yellow)

[Возможности](#-возможности) •
[Как это работает](#-как-это-работает) •
[Настройка Amvera](#-настройка-amvera) •
[Локальный запуск](#-локальный-запуск) •
[Структура](#-структура-проекта)

</div>

---

## ✨ Возможности

| | Функция | Статус |
|---|---|:---:|
| 👋 | Приветствие на `/start` | ✅ готово |
| 👥 | Выбор группы (3 группы) | 🔜 скоро |
| 📅 | Расписание на сегодня / завтра / неделю | 🔜 скоро |
| 📝 | Домашние задания по предметам | 🔜 скоро |
| ➕ | Добавление ДЗ | 🔜 скоро |

<details>
<summary>💬 Как выглядит ответ на <code>/start</code></summary>

```text
Привет, Саша! 👋
Я помощник твоей группы: скоро здесь будут расписание и домашка.
Рад знакомству! ✨
```

</details>

## 🔧 Как это работает

```text
Merge PR → ветка main на GitHub → Amvera пересобирает бота → бот отвечает в Telegram
```

- 🚀 **Автодеплой.** После мержа pull request'а в `main` Amvera сама забирает код,
  пересобирает и перезапускает бота.
- 💾 **Данные не теряются.** База — файл SQLite `/data/bot.db` в постоянном хранилище
  Amvera. Папка `/data` не стирается при пересборке, а файл базы не хранится в git,
  поэтому мержи данные не затирают.
- 🔐 **Секреты в безопасности.** Токен бота хранится только в секретах Amvera
  (и в `.env` при локальном запуске) и никогда не попадает в репозиторий.

## 🛠 Настройка Amvera

> [!NOTE]
> Всё ниже делается **один раз**. Дальше достаточно мержить pull request'ы.

<details>
<summary><b>1. 🤖 Токен бота</b></summary>

Напишите [@BotFather](https://t.me/BotFather) → `/newbot` → скопируйте токен.

</details>

<details>
<summary><b>2. 📦 Проект на Amvera</b></summary>

1. Войдите в [amvera.ru](https://amvera.ru/) → **Создать проект** → тип «Приложение».
2. Тариф: для начала хватит «Пробного».
3. Способ загрузки кода — через Git (подключим на шаге 4).
4. Настройки сборки менять не нужно: они берутся из [`amvera.yml`](amvera.yml).

</details>

<details>
<summary><b>3. 🔐 Переменные и секреты</b></summary>

Проект → **Переменные** → **Добавить переменные или секрет**:

| Название | Значение | Обязательно |
|---|---|:---:|
| `BOT_TOKEN` | токен от @BotFather (как **секрет**) | ✅ |
| `PYTHONUNBUFFERED` | `1` — чтобы логи появлялись сразу | рекомендуется |
| `TELEGRAM_PROXY` | `http://host:port` или `socks5://host:port` | только если Telegram недоступен напрямую |

> [!IMPORTANT]
> После изменения переменных перезапустите проект — иначе они не применятся.

</details>

<details>
<summary><b>4. 🔄 Автодеплой из GitHub</b></summary>

1. **Токен GitHub.** GitHub → Settings → Developer settings → Personal access tokens →
   **Tokens (classic)** → Generate new token. Право `repo`, срок — без истечения.
2. **В Amvera:** проект → вкладка **Репозиторий** → подключение GitHub:
   - событие: **Push**, ветка: **main**;
   - придумайте **секрет** (любая длинная строка), вставьте токен GitHub;
   - скопируйте показанный **URL** → **Применить**.
3. **В GitHub:** `botguu` → Settings → **Webhooks** → **Add webhook**:
   - Payload URL — URL из Amvera;
   - Content type — `application/json`;
   - Secret — тот же секрет, что в Amvera;
   - событие — **Just the push event** → **Add webhook**.

Подробнее — в [документации Amvera](https://docs.amvera.ru/applications/git/webhooks.html).

</details>

<details>
<summary><b>5. ✅ Проверка</b></summary>

1. Смёрджите pull request в `main` и дождитесь статуса «Успешно развернуто»
   (логи могут появляться с задержкой в несколько минут).
2. В логах должна быть строка `База данных: /data/bot.db`.
3. Напишите боту `/start`.

> [!TIP]
> Бот молчит, а в логах ошибки подключения к Telegram? Задайте `TELEGRAM_PROXY`
> и перезапустите проект.

</details>

## 💻 Локальный запуск

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # и впишите BOT_TOKEN
python bot.py
```

Локально база создаётся в файле `bot.db` в папке проекта.

> [!WARNING]
> Не запускайте бота локально, пока он работает на Amvera с тем же токеном:
> Telegram позволяет получать сообщения только одному экземпляру бота.

## 📁 Структура проекта

```text
botguu/
├── bot.py            # код бота
├── requirements.txt  # зависимости Python
├── amvera.yml        # настройки сборки и запуска на Amvera
├── .env.example      # пример переменных для локального запуска
├── CLAUDE.md         # правила работы над проектом
└── README.md         # вы здесь
```

---

<div align="center">
<sub>Сделано с ❤️ для студентов</sub>
</div>
