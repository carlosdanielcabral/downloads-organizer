# Organizador Inteligente de Downloads (v1)

Aplicativo Python em background que monitora a pasta Downloads do Windows, detecta downloads concluídos e move arquivos para subpastas organizadas por tipo.

## Funcionalidades

- Monitoramento automático da pasta Downloads
- Organização por tipo de arquivo (imagens, vídeos, áudios, documentos, outros)
- Bandeja do sistema com controles de pausar/retomar
- Tratamento de downloads incompletos (`.crdownload`, `.part`, `.tmp`, `.download`)
- Resolução automática de conflitos de nomes (arquivos duplicados)
- Criação automática das pastas de destino

## Instalação

1. Clone o repositório
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução

```bash
python -m src.main
```

## Categorias e Destinos

| Categoria | Pasta Destino | Extensões |
|-----------|---------------|-----------|
| Imagens | `Pictures/Downloads` | png, jpg, jpeg, gif, webp, bmp, svg, ico, tiff |
| Vídeos | `Videos/Downloads` | mp4, mkv, avi, mov, wmv, webm, flv |
| Áudios | `Music/Downloads` | mp3, wav, flac, ogg, m4a, aac, wma |
| Documentos | `Documents/Downloads` | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, md, csv, rtf, exe, msi, bat, cmd, ps1, zip, rar, 7z, tar, gz |
| Outros | `Downloads/Outros` | Extensões desconhecidas ou sem extensão |

**Nota:** Documentos, executáveis e arquivos compactados são movidos para uma única pasta `Documents/Downloads`.

## Controles da Bandeja

- **Status**: Exibe "Monitorando" ou "Pausado"
- **Pausar/Retomar**: Alterna o monitoramento da pasta Downloads
- **Sair**: Encerra o aplicativo

## Detalhes Técnicos

- Ignora arquivos de download incompleto (`.crdownload`, `.part`, `.tmp`, `.download`)
- Aguarda conclusão da escrita do arquivo antes de mover (debounce + verificação de lock)
- Tratamento de arquivos bloqueados por outros processos (até 15 tentativas com 2s de intervalo)
- Monitora apenas novos arquivos (eventos `on_created` e `on_moved`)

## Limitações Conhecidas (v1)

- Organização retroativa não implementada (apenas novos arquivos)
- Pasta monitorada hardcoded (`%USERPROFILE%\Downloads`)
- Se um arquivo permanecer aberto por mais de 30 segundos, a organização falha e o arquivo permanece em Downloads
- Não há notificações toast ao mover arquivos

## Roadmap (v2)

- Interface gráfica de configuração
- Edição do mapeamento extensão → pasta
- Seleção da pasta monitorada
- Organização de arquivos já existentes (scan retroativo)
- Fila de retry em background para arquivos que falharam por lock
- Início automático com o Windows
- Histórico/log visual
- Notificações toast

## Estrutura do Projeto

```
download-organizer/
├── src/
│   ├── main.py          # Ponto de entrada
│   ├── rules.py         # Extensão → categoria
│   ├── paths.py         # Categoria → pasta destino
│   ├── file_utils.py    # Operações genéricas de filesystem
│   ├── mover.py         # Orquestração da organização
│   ├── handler.py       # Handler de eventos do watchdog
│   ├── watcher.py       # Monitoramento da pasta
│   └── tray.py          # Bandeja do sistema
├── requirements.txt
└── README.md
```

## Teste Manual Sugerido

1. Inicie o aplicativo
2. Copie `teste.png` para Downloads → deve aparecer em `Pictures/Downloads/teste.png`
3. Copie `teste.png` novamente → deve virar `teste (1).png`
4. Copie `setup.exe` para Downloads → deve ir para `Documents/Downloads/setup.exe`
5. Baixe um arquivo real pelo Chrome → confirme que `.crdownload` é ignorado e o arquivo final é movido
6. Pause via bandeja → copie um arquivo → não deve mover
7. Retome → o próximo arquivo deve mover normalmente
