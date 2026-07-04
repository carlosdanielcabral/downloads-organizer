# Organizador Inteligente de Downloads

Aplicativo Python em background que monitora a pasta Downloads do Windows, detecta downloads concluídos e move arquivos para subpastas organizadas por tipo.

## Funcionalidades

- Monitoramento automático da pasta Downloads
- Organização por tipo de arquivo (imagens, vídeos, áudios, documentos, outros)
- **Interface gráfica** que abre automaticamente ao iniciar (CustomTkinter)
- **Seção Status** em tempo real: lista de arquivos pendentes com horário previsto de movimentação e botões para mover ou cancelar individualmente
- Edição de mapeamento extensão → categoria
- Edição de mapeamento categoria → pasta
- Seleção da pasta monitorada
- **Delay configurável** antes de mover arquivos (padrão: 30 minutos)
- **Notificações toast** ao organizar arquivos (opcional)
- Bandeja do sistema com controles de pausar/retomar, mover agora e configurações
- Clique esquerdo no ícone da bandeja abre a janela de configurações
- Tratamento de downloads incompletos (`.crdownload`, `.part`, `.tmp`, `.download`)
- Resolução automática de conflitos de nomes (arquivos duplicados)
- Criação automática das pastas de destino
- Hot reload do watcher ao salvar configurações

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

```bash
python main.py
```

A janela de configurações abre automaticamente. O aplicativo continua rodando em background via bandeja do sistema após fechar a janela.

## Interface Gráfica

### Abrir a janela

- A janela abre automaticamente ao iniciar o aplicativo
- Clique com o **botão esquerdo** no ícone da bandeja para reabrir
- Clique com o **botão direito** → "Configurações" para o mesmo efeito
- Apenas uma instância da janela é mantida aberta por vez

### Aba Monitoramento (padrão)

#### Seção Status

Exibe em tempo real os arquivos aguardando movimentação:
- Nome do arquivo e horário previsto de movimentação
- **Mover**: move o arquivo imediatamente, ignorando o delay restante
- **Cancelar**: remove o arquivo da fila, mantendo-o na pasta de origem
- **Mover Todos Agora**: move todos os arquivos pendentes de uma vez

A lista é atualizada automaticamente via Observer — sem polling.

#### Seção Configurações

- **Pasta Monitorada**: selecione a pasta a monitorar (padrão: `%USERPROFILE%\Downloads`)
- **Notificações**: habilita ou desabilita notificações toast ao organizar arquivos
- **Delay antes de mover**: tempo em minutos antes de mover um arquivo detectado (0 = imediato)

### Aba Pastas

Personalize as pastas de destino para cada categoria:
- **IMAGES**, **VIDEOS**, **AUDIO**, **DOCUMENTS**, **OTHER**
- Clique em "..." para selecionar via file dialog

### Aba Extensões

Visualize e edite o mapeamento de extensões para categorias:
- Lista scrollable com todas as extensões configuradas
- Dropdown por extensão: IMAGES, VIDEOS, AUDIO, DOCUMENTS, OTHER
- Botão "X" para remover uma extensão

### Salvar e Aplicar

Clique em "Salvar e Aplicar" para persistir todas as configurações em `config.json` e aplicar imediatamente ao watcher. A janela é fechada após salvar.

## Categorias e Destinos (Padrão)

| Categoria | Pasta Destino | Extensões |
|-----------|---------------|-----------|
| Imagens | `Imagens/Downloads` | png, jpg, jpeg, gif, webp, bmp, svg, ico, tiff |
| Vídeos | `Vídeos/Downloads` | mp4, mkv, avi, mov, wmv, webm, flv |
| Áudios | `Músicas/Downloads` | mp3, wav, flac, ogg, m4a, aac, wma |
| Documentos | `Documentos/Downloads` | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, csv, rtf, exe, msi, bat, cmd, ps1, zip, rar, 7z, tar, gz |
| Outros | `Downloads/Outros` | Extensões desconhecidas ou sem extensão |

## Controles da Bandeja

- **Status**: exibe "Monitorando" ou "Pausado"
- **Pausar/Retomar**: suspende ou retoma a detecção de novos arquivos (arquivos já agendados continuam na fila)
- **Mover Agora**: move todos os arquivos pendentes imediatamente
- **Configurações**: abre a janela de configurações
- **Sair**: encerra o aplicativo

## Detalhes Técnicos

- GUI e daemon rodam no mesmo processo — a seção Status acessa a fila diretamente via referência, sem IPC
- Reatividade via padrão Observer: `DelayQueue` notifica a GUI a cada mutação da fila; a GUI agenda a atualização com `after(0)` para garantir thread-safety no tkinter
- Ignora arquivos de download incompleto (`.crdownload`, `.part`, `.tmp`, `.download`)
- Aguarda conclusão da escrita antes de mover (debounce de 1.5s + verificação de lock)
- Tratamento de arquivos bloqueados por outros processos (até 15 tentativas com 2s de intervalo)
- Monitora apenas novos arquivos (eventos `on_created` e `on_moved`)
- Configurações persistem em `config.json` para edição manual
- Notificações toast via desktop-notifier (Windows 10/11)

## Estrutura do Projeto

```
download-organizer/
├── lib/                        # Lógica de negócio (core)
│   ├── config/
│   │   └── config.py           # Modelo de configuração
│   ├── processing/
│   │   ├── file_processor.py   # Orquestração: valida, agenda ou move
│   │   ├── file_mover.py       # Operação de movimentação
│   │   ├── paths.py            # Categoria → pasta destino
│   │   └── rules.py            # Extensão → categoria
│   ├── queue/
│   │   ├── delay_queue.py      # Fila de tarefas agendadas com Observer
│   │   ├── delayed_task.py     # Timer individual por arquivo
│   │   ├── file_queue.py       # Fila thread-safe de eventos do watcher
│   │   └── pending_file.py     # Snapshot imutável de arquivo pendente
│   ├── notifications/
│   │   └── notifications.py    # Notificações toast
│   ├── utils/
│   │   └── file_utils.py       # Operações genéricas de filesystem
│   └── watcher/
│       ├── file_event_handler.py  # Handler de eventos do watchdog
│       ├── file_event_watcher.py  # Monitoramento e ciclo de vida
│       └── file_event_watcher_factory.py  # Montagem das dependências
├── view/                       # Interface gráfica
│   ├── gui.py                  # Janela principal (ConfigWindow)
│   ├── gui_manager.py          # Singleton e thread da janela
│   ├── tray.py                 # Bandeja do sistema
│   ├── tabs/
│   │   ├── monitoring_tab.py   # Aba Monitoramento (Status + Configurações)
│   │   ├── folders_tab.py      # Aba Pastas
│   │   └── extensions_tab.py   # Aba Extensões
│   └── widgets/
│       └── file_picker.py      # Seletor de pasta reutilizável
├── main.py                     # Ponto de entrada
├── config.json                 # Configurações (criado em runtime)
├── default_config.json         # Configurações padrão
├── requirements.txt
└── README.md
```

## Teste Manual Sugerido

1. Inicie o aplicativo — a janela abre automaticamente
2. Na aba "Pastas", altere a pasta de imagens para uma pasta de teste e clique em "Salvar e Aplicar"
3. Reabra a janela clicando no ícone da bandeja (botão esquerdo)
4. Copie `teste.png` para a pasta monitorada — o arquivo deve aparecer na seção Status com o horário previsto
5. Clique em "Mover" na linha do arquivo — deve ser movido imediatamente para a pasta configurada
6. Copie `teste.png` novamente → deve virar `teste (1).png`
7. Copie um arquivo e clique em "Cancelar" — o arquivo deve ser removido da fila e permanecer em Downloads
8. Pause via bandeja → copie um arquivo → não deve entrar na fila
9. Retome → o próximo arquivo detectado deve ser agendado normalmente
