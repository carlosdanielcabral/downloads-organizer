# Downloads Organizer

<img width="2304" height="1836" alt="icon" src="https://github.com/user-attachments/assets/e6c30c0e-b4d6-43ad-aacc-2d4d9e3f37c8" />

## Descrição

Aplicativo Python em background que monitora a pasta Downloads do Windows, detecta downloads concluídos e move arquivos para subpastas organizadas por tipo.

## Funcionalidades

- Monitoramento automático da pasta Downloads
- Organização por tipo de arquivo (imagens, vídeos, áudios, documentos, outros)
- **Interface gráfica** que abre automaticamente ao iniciar (CustomTkinter)
- **Seção Status** em tempo real: lista de arquivos pendentes com horário previsto de movimentação e botões para mover ou cancelar individualmente
- **Histórico persistente** de arquivos movidos com retenção configurável (padrão: 30 dias)
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

### Via Python

```bash
python main.py
```

### Via executável

Para gerar um `.exe` standalone (requer `pyinstaller`):

```bash
pip install -r requirements-dev.txt
python build.py
```

O executável será gerado em `dist/DownloadOrganizer.exe`. O `config.json` e o `history.json` são criados automaticamente na mesma pasta do executável.

---

A janela de configurações abre automaticamente ao iniciar. O aplicativo continua rodando em background via bandeja do sistema após fechar a janela.

## Interface Gráfica

### Abrir a janela

- A janela abre automaticamente ao iniciar o aplicativo
- Clique com o **botão esquerdo** no ícone da bandeja para reabrir
- Clique com o **botão direito** → "Configurações" para o mesmo efeito
- Apenas uma instância da janela é mantida aberta por vez

### Aba Monitoramento (padrão)

<img width="716" height="514" alt="image" src="https://github.com/user-attachments/assets/463221aa-30eb-4996-ac45-35b5a9d6a10b" />

#### Seção Status

<img width="638" height="189" alt="image" src="https://github.com/user-attachments/assets/188a779e-5b27-4865-9050-6a1fea3de7b3" />

Exibe em tempo real os arquivos aguardando movimentação:
- Nome do arquivo e horário previsto de movimentação
- **Mover**: move o arquivo imediatamente, ignorando o delay restante
- **Cancelar**: remove o arquivo da fila, mantendo-o na pasta de origem
- **Mover Todos Agora**: move todos os arquivos pendentes de uma vez

A lista é atualizada automaticamente via Observer — sem polling.

#### Seção Histórico

<img width="626" height="148" alt="image" src="https://github.com/user-attachments/assets/9aedb0d0-f065-4236-ac86-09e10dac1bd8" />

Exibe os arquivos movidos dentro do período de retenção configurado:
- Formato: `nome_arquivo → /caminho/destino — DD/MM/YYYY HH:MM`
- Altura dinâmica: cresce com o conteúdo até um máximo, depois habilita scroll
- Persiste entre sessões em `history.json`
- Purge automático diário: entradas mais antigas que o período de retenção são removidas

#### Seção Configurações

<img width="635" height="257" alt="image" src="https://github.com/user-attachments/assets/43bf63b9-756a-4916-b599-f99548b6fa2a" />


- **Pasta Monitorada**: selecione a pasta a monitorar (padrão: `%USERPROFILE%\Downloads`)
- **Notificações**: habilita ou desabilita notificações toast ao organizar arquivos
- **Delay antes de mover**: tempo em minutos antes de mover um arquivo detectado (0 = imediato, apenas números)

### Aba Pastas

<img width="673" height="481" alt="image" src="https://github.com/user-attachments/assets/316f1c3c-188b-4964-81e0-6644d3e74b0a" />


Personalize as pastas de destino para cada categoria:
- **IMAGES**, **VIDEOS**, **AUDIO**, **DOCUMENTS**, **OTHER**
- Clique em "..." para selecionar via file dialog

### Aba Extensões

<img width="725" height="508" alt="image" src="https://github.com/user-attachments/assets/59223023-b828-4291-8553-09ba5dc82618" />


Visualize e edite o mapeamento de extensões para categorias:
- Lista scrollable com todas as extensões configuradas
- Dropdown por extensão: IMAGES, VIDEOS, AUDIO, DOCUMENTS, OTHER
- Botão "X" para remover uma extensão

### Rodapé

<img width="733" height="67" alt="image" src="https://github.com/user-attachments/assets/4ff6496e-7296-428b-80ed-10be38ad3794" />


- **Salvar e Aplicar**: persiste todas as configurações em `config.json`, aplica imediatamente ao watcher e fecha a janela
- **Parar** *(vermelho)*: encerra completamente o aplicativo

## Categorias e Destinos (Padrão)

| Categoria | Pasta Destino | Extensões |
|-----------|---------------|-----------|
| Imagens | `Imagens/Downloads` | png, jpg, jpeg, gif, webp, bmp, svg, ico, tiff |
| Vídeos | `Vídeos/Downloads` | mp4, mkv, avi, mov, wmv, webm, flv |
| Áudios | `Músicas/Downloads` | mp3, wav, flac, ogg, m4a, aac, wma |
| Documentos | `Documentos/Downloads` | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, csv, rtf, exe, msi, bat, cmd, ps1, zip, rar, 7z, tar, gz |
| Outros | `Downloads/Outros` | Extensões desconhecidas ou sem extensão |

## Controles da Bandeja

<img width="140" height="106" alt="image" src="https://github.com/user-attachments/assets/375e5f1e-a1ff-45f2-95d6-974425842a7a" />


- **Status**: exibe "Monitorando" ou "Pausado"
- **Pausar/Retomar**: suspende ou retoma a detecção de novos arquivos (arquivos já agendados continuam na fila)
- **Mover Agora**: move todos os arquivos pendentes imediatamente
- **Configurações**: abre a janela de configurações
- **Sair**: encerra o aplicativo

## Detalhes Técnicos

- GUI e daemon rodam no mesmo processo — a seção Status acessa a fila diretamente via referência, sem IPC
- Reatividade via padrão Observer: `DelayQueue` e `MoveHistory` notificam a GUI a cada mutação; a GUI agenda a atualização com `after(0)` para garantir thread-safety no tkinter
- Histórico persiste em `history.json`; purge automático via `threading.Timer` a cada 24h
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
│   ├── history/
│   │   ├── moved_file.py       # Dataclass de arquivo movido (serialização)
│   │   └── move_history.py     # Serviço de histórico com purge e Observer
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
│       ├── file_event_handler.py         # Handler de eventos do watchdog
│       ├── file_event_watcher.py         # Monitoramento e ciclo de vida
│       └── file_event_watcher_factory.py # Montagem das dependências
├── view/                       # Interface gráfica
│   ├── gui.py                  # Janela principal (ConfigWindow)
│   ├── gui_manager.py          # Singleton e thread da janela
│   ├── tray.py                 # Bandeja do sistema
│   ├── tabs/
│   │   ├── monitoring/
│   │   │   ├── monitoring_tab.py   # Aba Monitoramento
│   │   │   ├── status_section.py   # Seção de arquivos pendentes
│   │   │   ├── history_section.py  # Seção de histórico
│   │   │   └── settings_section.py # Seção de configurações
│   │   ├── folders/
│   │   │   └── folders_tab.py      # Aba Pastas
│   │   └── extensions/
│   │       └── extensions_tab.py   # Aba Extensões
│   └── widgets/
│       └── file_picker.py      # Seletor de pasta reutilizável
├── main.py                     # Ponto de entrada
├── build.py                    # Script para gerar o executável
├── config.json                 # Configurações (criado em runtime)
├── history.json                # Histórico de movimentações (criado em runtime)
├── default_config.json         # Configurações padrão
├── requirements.txt            # Dependências de runtime
├── requirements-dev.txt        # Dependências de desenvolvimento (PyInstaller)
└── README.md
```

## Teste Manual Sugerido

1. Inicie o aplicativo — a janela abre automaticamente
2. Na aba "Pastas", altere a pasta de imagens para uma pasta de teste e clique em "Salvar e Aplicar"
3. Reabra a janela clicando no ícone da bandeja (botão esquerdo)
4. Copie `teste.png` para a pasta monitorada — o arquivo deve aparecer na seção Status com o horário previsto
5. Clique em "Mover" na linha do arquivo — deve ser movido imediatamente para a pasta configurada
6. O arquivo movido deve aparecer na seção Histórico com nome, destino e horário
7. Copie `teste.png` novamente → deve virar `teste (1).png`
8. Copie um arquivo e clique em "Cancelar" — o arquivo deve ser removido da fila e permanecer em Downloads
9. Pause via bandeja → copie um arquivo → não deve entrar na fila
10. Retome → o próximo arquivo detectado deve ser agendado normalmente
