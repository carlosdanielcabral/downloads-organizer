# Organizador Inteligente de Downloads (v2)

Aplicativo Python em background que monitora a pasta Downloads do Windows, detecta downloads concluídos e move arquivos para subpastas organizadas por tipo.

## Funcionalidades

- Monitoramento automático da pasta Downloads
- Organização por tipo de arquivo (imagens, vídeos, áudios, documentos, outros)
- **Interface gráfica de configuração** (CustomTkinter)
- Edição de mapeamento extensão → categoria
- Edição de mapeamento categoria → pasta
- Seleção da pasta monitorada
- **Delay configurável** antes de mover arquivos (padrão: 30 minutos)
- **Botão "Mover Agora"** para mover arquivos pendentes imediatamente
- **Notificações toast** ao organizar arquivos (opcional)
- Bandeja do sistema com controles de pausar/retomar e configurações
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

## Configuração (v2)

O aplicativo possui uma interface gráfica para personalizar as regras de organização.

### Acessar Configurações

1. Clique com botão direito no ícone da bandeja do sistema
2. Selecione "Configurações"
3. A janela de configurações será aberta

### Aba Pastas

Personalize as pastas de destino para cada categoria:
- **IMAGES**: Pasta para imagens
- **VIDEOS**: Pasta para vídeos
- **AUDIO**: Pasta para áudios
- **DOCUMENTS**: Pasta para documentos
- **OTHER**: Pasta para arquivos desconhecidos

Clique no botão "..." para navegar e selecionar a pasta desejada.

### Aba Monitoramento

Selecione a pasta que deseja monitorar para novos downloads:
- Campo de texto com a pasta atual
- Botão "..." para selecionar pasta via file dialog
- Por padrão, monitora `%USERPROFILE%\Downloads`
- Checkbox para habilitar/desabilitar notificações toast ao organizar arquivos
- Campo para configurar o delay antes de mover arquivos (em minutos)
  - Por padrão: 30 minutos
  - Configure para 0 para mover imediatamente
  - Cada arquivo tem seu próprio timer individual

### Aba Extensões

Visualize e edite o mapeamento de extensões para categorias:
- Lista scrollable mostrando todas as extensões configuradas
- Selecione a categoria através de dropdown (IMAGES, VIDEOS, AUDIO, DOCUMENTS, OTHER)
- Remova extensões com o botão "X"
- As alterações são salvas ao clicar em "Salvar e Aplicar"

### Salvar e Aplicar

Clique em "Salvar e Aplicar" para:
- Salvar as configurações em `config.json`
- Reiniciar o monitoramento com as novas regras

### Arquivo de Configuração

As configurações são salvas em `config.json` na raiz do projeto. Você pode editar manualmente se preferir.

## Categorias e Destinos (Padrão)

| Categoria | Pasta Destino | Extensões |
|-----------|---------------|-----------|
| Imagens | `Imagens/Downloads` | png, jpg, jpeg, gif, webp, bmp, svg, ico, tiff |
| Vídeos | `Vídeos/Downloads` | mp4, mkv, avi, mov, wmv, webm, flv |
| Áudios | `Músicas/Downloads` | mp3, wav, flac, ogg, m4a, aac, wma |
| Documentos | `Documentos/Downloads` | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, csv, rtf, exe, msi, bat, cmd, ps1, zip, rar, 7z, tar, gz |
| Outros | `Downloads/Outros` | Extensões desconhecidas ou sem extensão |

**Nota:** Você pode personalizar esses mapeamentos através da interface gráfica.

## Controles da Bandeja

- **Status**: Exibe "Monitorando" ou "Pausado"
- **Pausar/Retomar**: Alterna o monitoramento da pasta
- **Mover Agora**: Move todos os arquivos pendentes imediatamente (ignora o delay)
- **Configurações**: Abre a interface gráfica de configuração
- **Sair**: Encerra o aplicativo

## Detalhes Técnicos

- Ignora arquivos de download incompleto (`.crdownload`, `.part`, `.tmp`, `.download`)
- Aguarda conclusão da escrita do arquivo antes de mover (debounce + verificação de lock)
- Tratamento de arquivos bloqueados por outros processos (até 15 tentativas com 2s de intervalo)
- Monitora apenas novos arquivos (eventos `on_created` e `on_moved`)
- Configurações persistem em JSON para fácil edição manual
- Notificações toast usam desktop-notifier para Windows 10/11
- Notificações informam o destino do arquivo organizado
- Delay configurável por arquivo para permitir acesso via navegador antes de mover
- Cada arquivo tem seu próprio timer individual para evitar sobrecarga

## Estrutura do Projeto

```
download-organizer/
├── lib/                      # Lógica de negócio (core)
│   ├── config.py            # Modelo de configuração
│   ├── rules.py             # Extensão → categoria
│   ├── paths.py             # Categoria → pasta destino
│   ├── file_utils.py        # Operações genéricas de filesystem
│   ├── mover.py             # Orquestração da organização
│   ├── notifications.py     # Notificações toast
│   ├── handler.py           # Handler de eventos do watchdog
│   └── watcher.py           # Monitoramento da pasta
├── view/                     # Interface gráfica
│   ├── gui.py               # Janela principal
│   ├── tray.py              # Bandeja do sistema
│   ├── tabs/                # Abas da GUI
│   │   ├── extensions_tab.py
│   │   ├── folders_tab.py
│   │   └── monitoring_tab.py
│   └── widgets/             # Componentes reutilizáveis
│       └── file_picker.py
├── main.py                   # Ponto de entrada
├── config.json              # Configurações (criado em runtime)
├── requirements.txt
└── README.md
```

## Teste Manual Sugerido

1. Inicie o aplicativo
2. Abra as configurações via bandeja
3. Na aba "Pastas", altere a pasta de imagens para uma pasta de teste
4. Clique em "Salvar e Aplicar"
5. Copie `teste.png` para Downloads → deve aparecer na pasta configurada
6. Copie `teste.png` novamente → deve virar `teste (1).png`
7. Na aba "Extensões", adicione uma nova extensão e teste
8. Pause via bandeja → copie um arquivo → não deve mover
9. Retome → o próximo arquivo deve mover normalmente
