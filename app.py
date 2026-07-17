<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GEOAGRESTE CRM - Licitações</title>
    
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

    <style>
        :root {
            --primary: #0f172a;
            --secondary: #3b82f6;
            --accent: #10b981;
            --danger: #ef4444;
            --warning: #f59e0b;
            --bg-color: #f1f5f9;
            --card-bg: #ffffff;
            --text-main: #1e293b;
            --text-muted: #64748b;
            --border: #e2e8f0;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', system-ui, sans-serif; }
        
        /* TELA DE LOGIN */
        #login-screen {
            position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
            background-color: var(--primary); display: flex; justify-content: center; align-items: center;
            z-index: 9999; flex-direction: column; color: white;
        }
        .login-box {
            background: white; padding: 40px; border-radius: 8px; width: 100%; max-width: 400px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5); color: var(--text-main);
        }
        .login-box h2 { margin-bottom: 20px; text-align: center; color: var(--primary); }
        .login-box input {
            width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid var(--border);
            border-radius: 5px; font-size: 1rem;
        }
        .login-box button {
            width: 100%; padding: 12px; background: var(--secondary); color: white;
            border: none; border-radius: 5px; font-size: 1.1rem; font-weight: bold; cursor: pointer;
        }
        .login-box button:hover { background: #2563eb; }
        #login-error { color: var(--danger); font-size: 0.9rem; text-align: center; margin-bottom: 10px; display: none; }

        /* Estrutura Principal Oculta Inicialmente */
        #app-container { display: none; height: 100vh; width: 100vw; overflow: hidden; background-color: var(--bg-color); color: var(--text-main); }
        .app-flex { display: flex; height: 100%; width: 100%; }

        /* Sidebar */
        aside { width: 250px; background-color: var(--primary); color: white; display: flex; flex-direction: column; }
        .logo-container { padding: 25px 20px; border-bottom: 1px solid #1e293b; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; }
        .logo-img { max-width: 80px; max-height: 80px; margin-bottom: 10px; border-radius: 8px; object-fit: contain; background: rgba(255,255,255,0.1); }
        .logo-text { font-size: 1.1rem; font-weight: 800; letter-spacing: 1px; color: #ffffff; }
        .logo-text span { color: var(--secondary); font-weight: 400; }
        nav { flex: 1; padding: 20px 0; }
        nav a { display: block; padding: 12px 20px; color: #cbd5e1; text-decoration: none; transition: 0.2s; cursor: pointer; }
        nav a:hover, nav a.active { background-color: #1e293b; color: white; border-left: 4px solid var(--secondary); }

        /* Main Content */
        main { flex: 1; display: flex; flex-direction: column; overflow-y: auto; padding: 30px; position: relative; }
        header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
        h1 { font-size: 1.8rem; color: var(--text-main); }
        .btn-primary { padding: 10px 20px; background: var(--secondary); color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: 600; transition: 0.2s; }
        .btn-primary:hover { background: #2563eb; }
        .view-section { display: none; }
        .view-section.active { display: block; }

        /* Dashboard Grid - Refletindo o Kanban */
        .dashboard-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 25px; }
        .card { background: var(--card-bg); padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); border: 1px solid var(--border); }
        .card h3 { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 10px; text-transform: uppercase; font-weight: bold; }
        .card .value { font-size: 2rem; font-weight: bold; color: var(--text-main); }
        .card.card-encontrada { border-left: 4px solid #64748b; }
        .card.card-analise { border-left: 4px solid var(--warning); }
        .card.card-doc { border-left: 4px solid var(--danger); }
        .card.card-disputa { border-left: 4px solid var(--secondary); }

        /* Dashboard Flex Area (Alertas + Mapa) */
        .dashboard-row { display: grid; grid-template-columns: 1fr 2fr; gap: 20px; margin-bottom: 25px; min-height: 400px; }
        .alerts-panel { background: var(--card-bg); padding: 20px; border-radius: 8px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: flex; flex-direction: column; }
        .alerts-title { font-weight: bold; font-size: 1.1rem; margin-bottom: 15px; color: var(--primary); display: flex; align-items: center; gap: 8px; }
        .alerts-list { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; max-height: 350px; }
        .alert-item { padding: 12px; border-radius: 6px; border-left: 4px solid; font-size: 0.85rem; line-height: 1.4; display: flex; flex-direction: column; gap: 4px; }
        .alert-item.urgent { background: #fee2e2; border-left-color: var(--danger); color: #991b1b; }
        .alert-item.warning { background: #fef3c7; border-left-color: var(--warning); color: #92400e; }
        .alert-item.info { background: #e0f2fe; border-left-color: var(--secondary); color: #075985; }

        .map-panel { background: var(--card-bg); border-radius: 8px; border: 1px solid var(--border); box-shadow: 0 1px 3px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
        .map-title { font-weight: bold; font-size: 1.1rem; padding: 20px 20px 10px; color: var(--primary); }
        #map { flex: 1; width: 100%; min-height: 320px; z-index: 1; }

        /* Kanban Board */
        .kanban-board { display: flex; gap: 15px; overflow-x: auto; padding-bottom: 20px; height: calc(100vh - 150px); }
        .kanban-column { background: #e2e8f0; min-width: 280px; width: 280px; border-radius: 8px; display: flex; flex-direction: column; padding: 10px; }
        .column-header { font-weight: bold; padding: 10px; margin-bottom: 10px; border-bottom: 2px solid #cbd5e1; display: flex; justify-content: space-between; }
        .column-header span { background: var(--primary); color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; }
        .kanban-cards { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; min-height: 100px; }
        
        .task-card { background: var(--card-bg); padding: 15px; border-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05); cursor: pointer; border-left: 4px solid var(--secondary); transition: 0.2s; }
        .task-card:hover { transform: translateY(-2px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .task-id { font-size: 0.75rem; color: var(--text-muted); margin-bottom: 5px; font-weight: 600; }
        .task-title { font-size: 0.95rem; font-weight: 600; margin-bottom: 8px; line-height: 1.3; }
        .task-org { font-size: 0.8rem; color: var(--text-muted); margin-bottom: 8px; display: flex; justify-content: space-between;}
        .task-date { font-size: 0.75rem; font-weight: bold; padding: 3px 6px; border-radius: 4px; background: #fef3c7; color: #b45309; display: inline-block; margin-bottom: 8px; }
        .task-date.expired { background: #fee2e2; color: #b91c1c; }
        .task-value { font-size: 0.9rem; font-weight: bold; color: var(--accent); }

        /* Modal (Ficha de Cadastro Completa) */
        .modal-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.6); display: none; justify-content: center; align-items: center; z-index: 1000; }
        .modal-overlay.active { display: flex; }
        .modal-content { background: white; width: 95%; max-width: 1000px; max-height: 90vh; border-radius: 8px; overflow-y: auto; padding: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.2); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border); padding-bottom: 15px; margin-bottom: 20px; }
        .modal-header h2 { font-size: 1.4rem; color: var(--primary); }
        .close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--text-muted); }
        
        .form-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; }
        .form-group { display: flex; flex-direction: column; margin-bottom: 10px; }
        .form-group.full-width { grid-column: span 3; }
        .form-group label { font-size: 0.80rem; font-weight: 600; color: var(--text-main); margin-bottom: 5px; }
        .form-group input, .form-group select, .form-group textarea { padding: 8px; border: 1px solid var(--border); border-radius: 5px; font-size: 0.9rem; outline: none; transition: 0.2s; }
        .form-group input:focus, .form-group textarea:focus, .form-group select:focus { border-color: var(--secondary); box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2); }
        .form-group textarea { resize: vertical; height: 80px; }
        
        .modal-footer { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; border-top: 1px solid var(--border); padding-top: 15px; }
        .btn-outline { padding: 10px 20px; background: white; color: var(--text-main); border: 1px solid var(--border); border-radius: 5px; cursor: pointer; font-weight: 600;}
        .btn-outline:hover { background: #f1f5f9; }
    </style>
</head>
<body>

    <!-- TELA DE LOGIN -->
    <div id="login-screen">
        <div class="logo-container" style="border:none; margin-bottom: 20px;">
            <div class="logo-text" style="font-size: 1.5rem;">GEOAGRESTE<br><span>Licitações</span></div>
        </div>
        <div class="login-box">
            <h2>Acesso Restrito</h2>
            <div id="login-error"></div>
            <form id="loginForm" onsubmit="realizarLogin(event)">
                <input type="text" id="username" placeholder="Usuário" required>
                <input type="password" id="password" placeholder="Senha" required>
                <button type="submit">Entrar no Sistema</button>
            </form>
        </div>
    </div>

    <!-- ESTRUTURA DO APLICATIVO -->
    <div id="app-container">
        <div class="app-flex">
            <aside>
                <div class="logo-container">
                    <img class="logo-img" id="companyLogo" src="https://placehold.co/100x100/1e293b/3b82f6?text=GEO" alt="Logo Geoagreste">
                    <div class="logo-text">GEOAGRESTE<br><span>Licitações</span></div>
                </div>
                <nav>
                    <a class="nav-link active" onclick="switchView('dashboard')">📊 Dashboard</a>
                    <a class="nav-link" onclick="switchView('kanban')">📋 Kanban (Workflow)</a>
                    <a class="nav-link" onclick="switchView('arquivadas')">🗄️ Arquivadas</a>
                    <a class="nav-link" onclick="logout()" style="margin-top: auto; color: #ef4444;">🚪 Sair</a>
                </nav>
            </aside>

            <main>
                <section id="dashboard" class="view-section active">
                    <header>
                        <h1>Visão Geral</h1>
                        <button class="btn-primary" onclick="openModal()">+ Nova Licitação</button>
                    </header>
                    
                    <div class="dashboard-grid" id="dashboard-stats">
                        <!-- Preenchido pelo JS com as 4 caixas do Kanban -->
                    </div>

                    <div class="dashboard-row">
                        <div class="alerts-panel">
                            <div class="alerts-title">⚠️ Alertas de Prazos</div>
                            <div class="alerts-list" id="alerts-container"></div>
                        </div>

                        <div class="map-panel">
                            <div class="map-title">📍 Localização das Oportunidades</div>
                            <div id="map"></div>
                        </div>
                    </div>
                </section>

                <section id="kanban" class="view-section">
                    <header>
                        <h1>Fluxo de Licitações</h1>
                        <button class="btn-primary" onclick="openModal()">+ Nova Licitação</button>
                    </header>
                    <div class="kanban-board" id="kanban-container"></div>
                </section>

                <section id="arquivadas" class="view-section">
                    <header>
                        <h1>Licitações Arquivadas</h1>
                    </header>
                    <div id="arquivadas-list" style="display: grid; gap: 10px;"></div>
                </section>
            </main>
        </div>
    </div>

    <!-- MODAL DE CADASTRO COM TODOS OS CAMPOS -->
    <div class="modal-overlay" id="bidModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 id="modalTitle">Ficha da Licitação Completa</h2>
                <button class="close-btn" type="button" onclick="closeModal()">×</button>
            </div>
            <form id="bidForm" onsubmit="saveBid(event)">
                <input type="hidden" id="bidId">
                
                <div class="form-grid">
                    <!-- Linha 1 -->
                    <div class="form-group">
                        <label>ID Contratação PNCP</label>
                        <input type="text" id="idPncp" placeholder="Ex: 13891130000103-1-000135/2026">
                    </div>
                    <div class="form-group">
                        <label>Fonte</label>
                        <input type="text" id="fonte" placeholder="Ex: Licitanet Licitações Eletrônicas">
                    </div>
                    <div class="form-group">
                        <label>Local / Município (Bahia)</label>
                        <input type="text" id="local" placeholder="Digite ou selecione o município..." list="municipios-bahia">
                        <datalist id="municipios-bahia">
                            <option value="Salvador/BA">
                            <option value="Vera Cruz/BA">
                            <option value="Camaçari/BA">
                            <option value="Feira de Santana/BA">
                            <option value="Vitória da Conquista/BA">
                            <option value="Juazeiro/BA">
                            <option value="Itabuna/BA">
                            <option value="Lauro de Freitas/BA">
                            <option value="Ilhéus/BA">
                            <option value="Jequié/BA">
                            <option value="Teixeira de Freitas/BA">
                            <option value="Alagoinhas/BA">
                            <option value="Barreiras/BA">
                            <option value="Porto Seguro/BA">
                            <option value="Simões Filho/BA">
                            <option value="Paulo Afonso/BA">
                            <option value="Eunápolis/BA">
                            <option value="Santo Antônio de Jesus/BA">
                            <option value="Valença/BA">
                            <option value="Luís Eduardo Magalhães/BA">
                            <option value="Guanambi/BA">
                            <option value="Jacobina/BA">
                            <option value="Serrinha/BA">
                            <option value="Itapetinga/BA">
                            <option value="Senhor do Bonfim/BA">
                            <option value="Brumado/BA">
                            <option value="Itaberaba/BA">
                            <option value="Irecê/BA">
                            <option value="Cruz das Almas/BA">
                            <option value="Bom Jesus da Lapa/BA">
                            <option value="Dias d'Ávila/BA">
                            <option value="Barra/BA">
                            <option value="Santo Amaro/BA">
                            <option value="Tucano/BA">
                            <option value="Conceição do Coité/BA">
                            <option value="Euclides da Cunha/BA">
                            <option value="Ipiaú/BA">
                            <option value="Jaguaquara/BA">
                            <option value="Casa Nova/BA">
                            <option value="Itamaraju/BA">
                            <option value="Campo Formoso/BA">
                            <option value="Inhambupe/BA">
                            <option value="Jeremoabo/BA">
                            <option value="Macaúbas/BA">
                            <option value="Maracás/BA">
                            <option value="Monte Santo/BA">
                            <option value="Morro do Chapéu/BA">
                            <option value="Mucuri/BA">
                            <option value="Mundo Novo/BA">
                            <option value="Muritiba/BA">
                            <option value="Nova Viçosa/BA">
                            <option value="Olindina/BA">
                            <option value="Poções/BA">
                            <option value="Queimadas/BA">
                            <option value="Remanso/BA">
                            <option value="Riachão do Jacuípe/BA">
                            <option value="Ribeira do Pombal/BA">
                            <option value="Rio Real/BA">
                            <option value="Ruy Barbosa/BA">
                            <option value="Santa Maria da Vitória/BA">
                            <option value="Santana/BA">
                            <option value="Santo Estêvão/BA">
                            <option value="Seabra/BA">
                            <option value="Sento Sé/BA">
                            <option value="Sobradinho/BA">
                            <option value="Amargosa/BA">
                            <option value="Catu/BA">
                            <option value="Gandú/BA">
                            <option value="Camamu/BA">
                            <option value="Canavieiras/BA">
                            <option value="Belmonte/BA">
                            <option value="Barra do Choça/BA">
                            <option value="Cansanção/BA">
                            <option value="Cícero Dantas/BA">
                            <option value="Itiúba/BA">
                            <option value="Livramento de Nossa Senhora/BA">
                            <option value="Mata de São João/BA">
                            <option value="Prado/BA">
                            <option value="Riacho de Santana/BA">
                            <option value="São Sebastião do Passé/BA">
                            <option value="Sátiro Dias/BA">
                            <option value="Ubaitaba/BA">
                            <option value="Ubatã/BA">
                            <option value="Valente/BA">
                            <option value="Wenceslau Guimarães/BA">
                            <option value="Xique-Xique/BA">
                        </datalist>
                    </div>

                    <!-- Linha 2 -->
                    <div class="form-group">
                        <label>Órgão</label>
                        <input type="text" id="orgao" placeholder="Ex: MUNICIPIO DE VERA CRUZ">
                    </div>
                    <div class="form-group" style="grid-column: span 2;">
                        <label>Unidade Compradora</label>
                        <input type="text" id="unidadeCompradora" placeholder="Ex: 3343 - MUNICÍPIO DE VERA CRUZ/BA">
                    </div>

                    <!-- Linha 3 -->
                    <div class="form-group">
                        <label>Modalidade da contratação</label>
                        <input type="text" id="modalidade" placeholder="Ex: Pregão - Eletrônico">
                    </div>
                    <div class="form-group">
                        <label>Amparo legal</label>
                        <input type="text" id="amparoLegal" placeholder="Ex: Lei 14.133/2021, Art. 28, I">
                    </div>
                    <div class="form-group">
                        <label>Tipo</label>
                        <input type="text" id="tipo" placeholder="Ex: Edital">
                    </div>

                    <!-- Linha 4 -->
                    <div class="form-group">
                        <label>Modo de disputa</label>
                        <input type="text" id="modoDisputa" placeholder="Ex: Aberto-Fechado">
                    </div>
                    <div class="form-group">
                        <label>Registro de preço</label>
                        <select id="registroPreco">
                            <option value="Não">Não</option>
                            <option value="Sim">Sim</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Fonte orçamentária</label>
                        <input type="text" id="fonteOrcamentaria" placeholder="Ex: Não informada">
                    </div>

                    <!-- Linha 5 -->
                    <div class="form-group">
                        <label>Data de divulgação no PNCP</label>
                        <input type="date" id="dataDivulgacao">
                    </div>
                    <div class="form-group">
                        <label>Situação</label>
                        <input type="text" id="situacao" placeholder="Ex: Divulgada no PNCP">
                    </div>
                    <div class="form-group">
                        <label>Status no Kanban (Funil Interno)</label>
                        <select id="status">
                            <option value="encontrada">Encontrada</option>
                            <option value="analise">Em Análise</option>
                            <option value="documentacao">Documentação</option>
                            <option value="disputa">Disputa / Sessão</option>
                            <option value="homologada">Homologada / Contrato</option>
                            <option value="arquivada">Arquivada (Perdida/Vencida)</option>
                        </select>
                    </div>

                    <!-- Linha 6 -->
                    <div class="form-group">
                        <label>Início recebimento propostas</label>
                        <input type="datetime-local" id="dataInicioPropostas">
                    </div>
                    <div class="form-group">
                        <label>Fim de recebimento de propostas</label>
                        <input type="datetime-local" id="dataFim">
                    </div>
                    <div class="form-group">
                        <label>Alerta Limite de Documentação</label>
                        <input type="datetime-local" id="dataDoc">
                    </div>

                    <!-- Linha 7 -->
                    <div class="form-group full-width">
                        <label>Valor Estimado (R$)</label>
                        <input type="number" id="valor" step="0.01" placeholder="Ex: 150000.00" style="width: 33%;">
                    </div>

                    <!-- Linha 8 -->
                    <div class="form-group full-width">
                        <label>Objeto da Licitação</label>
                        <textarea id="objeto" placeholder="Descreva o objeto da licitação..."></textarea>
                    </div>
                </div>

                <div class="modal-footer">
                    <button type="button" class="btn-outline" id="btnExcluirModal" onclick="excluirLicitacaoDirect(document.getElementById('bidId').value)" style="background:var(--danger); color:white; border:none; display:none; margin-right: auto;">❌ Excluir Permanentemente</button>
                    <button type="button" class="btn-outline" onclick="closeModal()">Cancelar</button>
                    <button type="submit" class="btn-primary">Salvar Licitação</button>
                </div>
            </form>
        </div>
    </div>

    <script>
        // CONFIGURAÇÕES GERAIS E API
        const API_URL = 'https://licitacao-ge9p.onrender.com/api'; // Aponta para a própria hospedagem
        let licitacoes = [];
        let map;
        let markersGroup;

        // SISTEMA DE LOGIN
        async function realizarLogin(e) {
            e.preventDefault();
            const u = document.getElementById('username').value;
            const p = document.getElementById('password').value;
            const err = document.getElementById('login-error');

            try {
                const response = await fetch(`${API_URL}/login`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: u, password: p })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    document.getElementById('login-screen').style.display = 'none';
                    document.getElementById('app-container').style.display = 'block';
                    carregarDadosDaAPI();
                } else {
                    err.innerText = data.message;
                    err.style.display = 'block';
                }
            } catch (error) {
                err.innerText = "Erro ao conectar com o servidor.";
                err.style.display = 'block';
            }
        }

        function logout() {
            document.getElementById('login-screen').style.display = 'flex';
            document.getElementById('app-container').style.display = 'none';
            document.getElementById('loginForm').reset();
            document.getElementById('login-error').style.display = 'none';
        }

        // CARREGAR DADOS DO BACKEND
        async function carregarDadosDaAPI() {
            try {
                const response = await fetch(`${API_URL}/licitacoes`);
                licitacoes = await response.json();
                renderAll();
            } catch (e) {
                console.error("Erro ao buscar dados", e);
                alert("Erro ao buscar dados do servidor!");
            }
        }

        const coordenadasMunicipios = {
            "salvador/ba": [-12.9714, -38.5014], "salvador": [-12.9714, -38.5014],
            "vera cruz/ba": [-12.9614, -38.6147], "vera cruz": [-12.9614, -38.6147],
            "camaçari": [-12.6975, -38.3242], "camaçari/ba": [-12.6975, -38.3242],
            "feira de santana": [-12.2664, -38.9662], "feira de santana/ba": [-12.2664, -38.9662],
            "vitória da conquista": [-14.8661, -40.8394], "vitória da conquista/ba": [-14.8661, -40.8394],
            "juazeiro": [-9.4116, -40.5033], "juazeiro/ba": [-9.4116, -40.5033],
            "itabuna": [-14.7914, -39.2800], "itabuna/ba": [-14.7914, -39.2800],
            "lauro de freitas": [-12.8944, -38.3308], "lauro de freitas/ba": [-12.8944, -38.3308],
            "ilhéus": [-14.7935, -39.0464], "ilhéus/ba": [-14.7935, -39.0464],
            "jequié": [-13.8584, -40.0821], "jequié/ba": [-13.8584, -40.0821],
            "teixeira de freitas": [-17.5361, -39.7419], "teixeira de freitas/ba": [-17.5361, -39.7419],
            "alagoinhas": [-12.1356, -38.4250], "alagoinhas/ba": [-12.1356, -38.4250],
            "barreiras": [-12.1528, -45.0031], "barreiras/ba": [-12.1528, -45.0031],
            "porto seguro": [-16.4497, -39.0647], "porto seguro/ba": [-16.4497, -39.0647],
            "simões filho": [-12.7844, -38.4011], "simões filho/ba": [-12.7844, -38.4011],
            "paulo afonso": [-9.4072, -38.2192], "paulo afonso/ba": [-9.4072, -38.2192],
            "eunápolis": [-16.3711, -39.5858], "eunápolis/ba": [-16.3711, -39.5858],
            "santo antônio de jesus": [-12.9689, -39.2619], "santo antônio de jesus/ba": [-12.9689, -39.2619],
            "valença": [-13.3703, -39.0731], "valença/ba": [-13.3703, -39.0731],
            "luís eduardo magalhães": [-12.0964, -45.7967], "luís eduardo magalhães/ba": [-12.0964, -45.7967],
            "guanambi": [-14.2233, -42.7814], "guanambi/ba": [-14.2233, -42.7814],
            "jacobina": [-11.1808, -40.5181], "jacobina/ba": [-11.1808, -40.5181],
            "serrinha": [-11.6642, -39.0075], "serrinha/ba": [-11.6642, -39.0075],
            "itapetinga": [-15.2481, -40.2478], "itapetinga/ba": [-15.2481, -40.2478],
            "senhor do bonfim": [-10.4614, -40.1878], "senhor do bonfim/ba": [-10.4614, -40.1878],
            "brumado": [-14.2028, -41.6669], "brumado/ba": [-14.2028, -41.6669],
            "itaberaba": [-12.5275, -40.3064], "itaberaba/ba": [-12.5275, -40.3064],
            "irecê": [-11.3042, -41.8569], "irecê/ba": [-11.3042, -41.8569],
            "cruz das almas": [-12.6711, -39.1022], "cruz das almas/ba": [-12.6711, -39.1022],
            "bom jesus da lapa": [-13.2575, -43.4181], "bom jesus da lapa/ba": [-13.2575, -43.4181],
            "dias d'ávila": [-12.6975, -38.3242], "dias d'ávila/ba": [-12.6975, -38.3242]
        };

        const colunas = [
            { id: 'encontrada', nome: 'Encontrada' },
            { id: 'analise', nome: 'Em Análise' },
            { id: 'documentacao', nome: 'Documentação' },
            { id: 'disputa', nome: 'Disputa / Sessão' },
            { id: 'homologada', nome: 'Homologada / Contrato' }
        ];

        function formatarMoeda(valor) {
            return parseFloat(valor || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
        }

        function formatarData(dataISO) {
            if (!dataISO) return "Não informada";
            const data = new Date(dataISO);
            return data.toLocaleDateString('pt-BR') + ' às ' + data.toLocaleTimeString('pt-BR', {hour: '2-digit', minute:'2-digit'});
        }

        // MAPA
        function initMap() {
            if (map) return; 
            map = L.map('map').setView([-12.9714, -38.5014], 8);
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { attribution: '© OpenStreetMap' }).addTo(map);
            markersGroup = L.layerGroup().addTo(map);
        }

        function renderMapMarkers() {
            if (!markersGroup) return;
            markersGroup.clearLayers();
            const ativas = licitacoes.filter(l => l.status !== 'arquivada' && l.status !== 'homologada');
            ativas.forEach(lic => {
                const localLower = lic.local ? lic.local.toLowerCase().trim() : '';
                let coordenadas = coordenadasMunicipios[localLower];
                if (!coordenadas) coordenadas = [-12.9714 + (Math.random() - 0.5) * 0.5, -38.5014 + (Math.random() - 0.5) * 0.5];
                L.marker(coordenadas).addTo(markersGroup).bindPopup(`
                    <strong>${lic.orgao || 'Não informado'}</strong><br>${(lic.objeto || '').substring(0, 50)}...<br>
                    <strong>Valor:</strong> ${formatarMoeda(lic.valor)}
                `);
            });
        }

        // ALERTAS
        function renderAlerts() {
            const container = document.getElementById('alerts-container');
            container.innerHTML = '';
            const hoje = new Date();
            const ativas = licitacoes.filter(l => l.status !== 'arquivada' && l.status !== 'homologada');

            if (ativas.length === 0) {
                container.innerHTML = '<div style="color: var(--text-muted); font-size: 0.9rem;">Sem pendências.</div>';
                return;
            }

            ativas.forEach(lic => {
                if (!lic.dataDoc) return;
                const diferencaHoras = (new Date(lic.dataDoc) - hoje) / (1000 * 60 * 60);
                let statusAlert = '', textAlert = '';

                if (diferencaHoras < 0) {
                    statusAlert = 'urgent';
                    textAlert = `⚠️ <b>ATRASADA!</b> O prazo de documento para ${lic.orgao || 'Sem Órgão'} expirou.`;
                } else if (diferencaHoras <= 48) {
                    statusAlert = 'warning';
                    textAlert = `⏳ <b>URGENTE:</b> Docs para ${lic.orgao || 'Sem Órgão'} vencem em ${Math.ceil(diferencaHoras)}h!`;
                } else {
                    statusAlert = 'info';
                    textAlert = `ℹ️ Docs de ${lic.orgao || 'Sem Órgão'} no prazo (Vence ${formatarData(lic.dataDoc)}).`;
                }

                container.innerHTML += `<div class="alert-item ${statusAlert}" onclick="abrirEdicao('${lic.uid}')" style="cursor:pointer">${textAlert}</div>`;
            });
        }

        // DASHBOARD (Refletindo o Kanban)
        function renderDashboard() {
            const qtdEncontrada = licitacoes.filter(l => l.status === 'encontrada').length;
            const qtdAnalise = licitacoes.filter(l => l.status === 'analise').length;
            const qtdDoc = licitacoes.filter(l => l.status === 'documentacao').length;
            const qtdDisputa = licitacoes.filter(l => l.status === 'disputa').length;

            document.getElementById('dashboard-stats').innerHTML = `
                <div class="card card-encontrada">
                    <h3>Encontrada</h3>
                    <div class="value">${qtdEncontrada}</div>
                </div>
                <div class="card card-analise">
                    <h3>Em Análise</h3>
                    <div class="value">${qtdAnalise}</div>
                </div>
                <div class="card card-doc">
                    <h3>Documentação</h3>
                    <div class="value">${qtdDoc}</div>
                </div>
                <div class="card card-disputa">
                    <h3>Disputa / Sessão</h3>
                    <div class="value">${qtdDisputa}</div>
                </div>
            `;
            
            renderAlerts();
            initMap();
            renderMapMarkers();
            setTimeout(() => { if (map) map.invalidateSize(); }, 200);
        }

        // KANBAN
        function renderKanban() {
            const container = document.getElementById('kanban-container');
            container.innerHTML = '';

            colunas.forEach(col => {
                const itens = licitacoes.filter(l => l.status === col.id);
                container.innerHTML += `
                    <div class="kanban-column" ondrop="drop(event, '${col.id}')" ondragover="allowDrop(event)">
                        <div class="column-header">${col.nome} <span>${itens.length}</span></div>
                        <div class="kanban-cards">
                            ${itens.map(lic => {
                                const isExpired = lic.dataFim && new Date(lic.dataFim) < new Date() ? 'expired' : '';
                                return `
                                <div class="task-card" draggable="true" ondragstart="drag(event, '${lic.uid}')" onclick="abrirEdicao('${lic.uid}')">
                                    <div class="task-id">${lic.idPncp || 'Sem ID'}</div>
                                    <div class="task-title">${(lic.objeto || 'Sem Objeto definido').substring(0, 50)}...</div>
                                    <div class="task-org"><b>${lic.orgao || 'Não informado'}</b> <span>${lic.local || ''}</span></div>
                                    <div class="task-date ${isExpired}">Sessão: ${formatarData(lic.dataFim)}</div>
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px; border-top: 1px solid var(--border); padding-top: 8px;">
                                        <div class="task-value">${formatarMoeda(lic.valor)}</div>
                                        <div style="display: flex; gap: 8px;">
                                            <button type="button" onclick="event.stopPropagation(); abrirEdicao('${lic.uid}')" title="Editar" style="background:none; border:none; cursor:pointer; font-size:1rem;">✏️</button>
                                            <button type="button" onclick="event.stopPropagation(); arquivarLicitacaoDirect('${lic.uid}')" title="Arquivar" style="background:none; border:none; cursor:pointer; font-size:1rem;">🗄️</button>
                                            <button type="button" onclick="event.stopPropagation(); excluirLicitacaoDirect('${lic.uid}')" title="Excluir" style="background:none; border:none; cursor:pointer; font-size:1rem;">❌</button>
                                        </div>
                                    </div>
                                </div>
                            `}).join('')}
                        </div>
                    </div>
                `;
            });
            renderArquivadas();
        }

        function renderArquivadas() {
            const container = document.getElementById('arquivadas-list');
            const itens = licitacoes.filter(l => l.status === 'arquivada');
            if(itens.length === 0) { container.innerHTML = '<p>Nenhuma licitação arquivada no momento.</p>'; return; }

            container.innerHTML = itens.map(lic => `
                <div class="card" style="display:flex; justify-content: space-between; align-items: center; border-left: 4px solid #64748b; margin-bottom: 10px;">
                    <div>
                        <div class="task-id">${lic.idPncp || 'Sem ID'}</div>
                        <strong>${lic.orgao || 'Sem Órgão'}</strong> - ${(lic.objeto||'').substring(0, 60)}...
                        <div class="task-date expired">Prazo Finalizado: ${formatarData(lic.dataFim)}</div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div>${formatarMoeda(lic.valor)}</div>
                        <button class="btn-outline" onclick="abrirEdicao('${lic.uid}')">Ver Detalhes</button>
                        <button class="btn-outline" style="background:var(--danger); color:white; border:none;" onclick="excluirLicitacaoDirect('${lic.uid}')">❌ Deletar</button>
                    </div>
                </div>
            `).join('');
        }

        // DRAG AND DROP COM SALVAMENTO NO BACKEND
        function allowDrop(ev) { ev.preventDefault(); }
        function drag(ev, uid) { ev.dataTransfer.setData("uid", uid); }
        async function drop(ev, novoStatus) {
            ev.preventDefault();
            const uid = ev.dataTransfer.getData("uid");
            const licIndex = licitacoes.findIndex(l => l.uid === uid);
            
            if(licIndex > -1) {
                licitacoes[licIndex].status = novoStatus;
                renderAll(); // Atualiza tela imediatamente

                // Manda pro servidor
                try {
                    await fetch(`${API_URL}/licitacoes/${uid}/status`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ status: novoStatus })
                    });
                } catch(e) { console.error(e); }
            }
        }

        // FUNÇÃO DE ARQUIVAMENTO DIRETO (BOTÃO DO KANBAN)
        async function arquivarLicitacaoDirect(uid) {
            if (!uid) return;
            const idx = licitacoes.findIndex(l => l.uid === uid);
            if (idx > -1) {
                licitacoes[idx].status = 'arquivada';
                renderAll();
                try {
                    await fetch(`${API_URL}/licitacoes/${uid}/status`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ status: 'arquivada' })
                    });
                } catch (e) { console.error("Erro ao arquivar", e); }
            }
        }

        // FUNÇÃO DE EXCLUSÃO DE LICITAÇÃO
        async function excluirLicitacaoDirect(uid) {
            if (!uid) return;
            if (confirm("Deseja realmente excluir esta licitação permanentemente do sistema?")) {
                licitacoes = licitacoes.filter(l => l.uid !== uid);
                renderAll();
                closeModal();
                try {
                    await fetch(`${API_URL}/licitacoes/${uid}`, {
                        method: 'DELETE'
                    });
                } catch (e) { console.error("Erro ao excluir do servidor", e); }
            }
        }

        // MODAL
        function openModal() {
            document.getElementById('bidForm').reset();
            document.getElementById('bidId').value = '';
            document.getElementById('btnExcluirModal').style.display = 'none';
            document.getElementById('modalTitle').innerText = 'Nova Licitação Completa';
            document.getElementById('bidModal').classList.add('active');
        }

        function closeModal() { document.getElementById('bidModal').classList.remove('active'); }

        function abrirEdicao(uid) {
            const lic = licitacoes.find(l => l.uid === uid);
            if(!lic) return;
            
            // Preencher todos os campos
            document.getElementById('bidId').value = lic.uid || '';
            document.getElementById('idPncp').value = lic.idPncp || '';
            document.getElementById('fonte').value = lic.fonte || '';
            document.getElementById('local').value = lic.local || '';
            document.getElementById('orgao').value = lic.orgao || '';
            document.getElementById('unidadeCompradora').value = lic.unidadeCompradora || '';
            document.getElementById('modalidade').value = lic.modalidade || '';
            document.getElementById('amparoLegal').value = lic.amparoLegal || '';
            document.getElementById('tipo').value = lic.tipo || '';
            document.getElementById('modoDisputa').value = lic.modoDisputa || '';
            document.getElementById('registroPreco').value = lic.registroPreco || 'Não';
            document.getElementById('fonteOrcamentaria').value = lic.fonteOrcamentaria || '';
            document.getElementById('dataDivulgacao').value = lic.dataDivulgacao || '';
            document.getElementById('situacao').value = lic.situacao || '';
            document.getElementById('status').value = lic.status || 'encontrada';
            document.getElementById('dataInicioPropostas').value = lic.dataInicioPropostas || '';
            document.getElementById('dataFim').value = lic.dataFim || '';
            document.getElementById('dataDoc').value = lic.dataDoc || '';
            document.getElementById('valor').value = lic.valor || '';
            document.getElementById('objeto').value = lic.objeto || '';
            
            document.getElementById('btnExcluirModal').style.display = 'inline-block';
            document.getElementById('modalTitle').innerText = 'Editar Licitação: ' + (lic.idPncp || 'Ficha');
            document.getElementById('bidModal').classList.add('active');
        }

        async function saveBid(event) {
            event.preventDefault();
            
            const novaLicitacao = {
                uid: document.getElementById('bidId').value || Date.now().toString(),
                idPncp: document.getElementById('idPncp').value,
                fonte: document.getElementById('fonte').value,
                local: document.getElementById('local').value,
                orgao: document.getElementById('orgao').value,
                unidadeCompradora: document.getElementById('unidadeCompradora').value,
                modalidade: document.getElementById('modalidade').value,
                amparoLegal: document.getElementById('amparoLegal').value,
                tipo: document.getElementById('tipo').value,
                modoDisputa: document.getElementById('modoDisputa').value,
                registroPreco: document.getElementById('registroPreco').value,
                fonteOrcamentaria: document.getElementById('fonteOrcamentaria').value,
                dataDivulgacao: document.getElementById('dataDivulgacao').value,
                situacao: document.getElementById('situacao').value,
                status: document.getElementById('status').value,
                dataInicioPropostas: document.getElementById('dataInicioPropostas').value,
                dataFim: document.getElementById('dataFim').value,
                dataDoc: document.getElementById('dataDoc').value,
                valor: document.getElementById('valor').value,
                objeto: document.getElementById('objeto').value
            };

            // Atualiza array local
            const index = licitacoes.findIndex(l => l.uid === novaLicitacao.uid);
            if (index > -1) licitacoes[index] = novaLicitacao;
            else licitacoes.push(novaLicitacao);

            // Manda pro servidor
            try {
                await fetch(`${API_URL}/licitacoes`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(novaLicitacao)
                });
            } catch(e) { console.error("Erro ao salvar", e); }

            closeModal();
            renderAll();
        }

        // NAVEGAÇÃO E ATUALIZAÇÃO GERAL
        function switchView(viewId) {
            document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
            document.querySelectorAll('.nav-link').forEach(nav => nav.classList.remove('active'));
            document.getElementById(viewId).classList.add('active');
            
            document.querySelectorAll('.nav-link').forEach(link => {
                if (link.getAttribute('onclick').includes(viewId)) link.classList.add('active');
            });
            if (viewId === 'dashboard') setTimeout(() => { if (map) map.invalidateSize(); }, 200);
        }

        function renderAll() {
            renderDashboard();
            renderKanban();
        }
    </script>
</body>
</html>