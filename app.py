import streamlit as st
from datetime import datetime

def definir_categorias():
    return {
        "Azeite Virgem Extra": {
            "acidez": (None, 0.80),
            "peroxidos": (None, 20.0),
            "k232": (None, 2.50),
            "k270": (None, 0.22),
            "delta_k": (None, 0.01)
        },
        "Azeite Virgem": {
            "acidez": (None, 2.00),
            "peroxidos": (None, 20.0),
            "k232": (None, 2.60),
            "k270": (None, 0.25),
            "delta_k": (None, 0.01)
        },
        "Azeite Refinado": {
            "acidez": (None, 0.30),
            "peroxidos": (None, 5.00),
            "k232": None,
            "k270": (None, 1.25),
            "delta_k": (None, 0.016)
        },
        "Azeite Composto": {
            "acidez": (None, 1.00),
            "peroxidos": (None, 15.00),
            "k232": None,
            "k270": (None, 1.15),
            "delta_k": (None, 0.015)
        },
        "Óleo de Bagaço de Azeitona Refinado": {
            "acidez": (None, 0.30),
            "peroxidos": (None, 5.00),
            "k232": None,
            "k270": (None, 2.00),
            "delta_k": (None, 0.020)
        },
        "Óleo de Bagaço de Azeitona": {
            "acidez": (None, 1.00),
            "peroxidos": (None, 15.00),
            "k232": None,
            "k270": (None, 1.70),
            "delta_k": (None, 0.018)
        },
        "Azeite Lampante": {
            "acidez": (2.00, None),
            "peroxidos": None,
            "k232": None,
            "k270": None,
            "delta_k": None
        },
        "Óleo de Bagaço de Azeitona Bruto": {
            "acidez": None,
            "peroxidos": None,
            "k232": None,
            "k270": None,
            "delta_k": None
        }
    }

def classificar_azeite(valores):
    """
    Classifica o azeite baseado nos valores fornecidos.
    """
    categorias = definir_categorias()
    resultado = {
        "classificacao": None,
        "detalhes": {},
        "valores_medidos": valores,
        "parametros_analisados": list(valores.keys())
    }
    
    # Renomear k268 para k270 se existir
    if 'k268' in valores:
        valores['k270'] = valores.pop('k268')
    
    for categoria, limites in categorias.items():
        conforme = True
        detalhes = {}
        
        for param in valores.keys():
            limite = limites[param]
            if limite is None:
                detalhes[param] = "Sem limite"
                continue
                
            valor = valores[param]
            min_val, max_val = limite
            
            if min_val is not None and valor <= min_val:
                conforme = False
                detalhes[param] = f"Abaixo do mínimo ({min_val})"
            elif max_val is not None and valor > max_val:
                conforme = False
                detalhes[param] = f"Acima do máximo ({max_val})"
            else:
                detalhes[param] = "Conforme"
        
        if conforme:
            resultado["classificacao"] = categoria
            resultado["detalhes"] = detalhes
            break
                
    if resultado["classificacao"] is None:
        resultado["classificacao"] = "Não classificado"
            
    return resultado

def main():
    st.set_page_config(page_title="Classificador de Azeite", layout="wide")
    
    st.title("Classificador de Azeite")
    st.write("Sistema de classificação segundo o Regulamento Delegado (UE) 2022/2104")
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        st.subheader("Dados da Amostra")
        num_amostra = st.text_input("Número da Amostra")
        
        analisar_acidez = st.checkbox("Analisar Acidez")
        analisar_peroxidos = st.checkbox("Analisar Índice de Peróxidos")
        analisar_ks = st.checkbox("Analisar Parâmetros K")
        
        valores = {}
        
        if analisar_acidez:
            st.subheader("Acidez")
            acidez = st.number_input("Acidez (%)", min_value=0.0, format="%.3f")
            if acidez >= 0:
                valores['acidez'] = acidez
        
        if analisar_peroxidos:
            st.subheader("Índice de Peróxidos")
            peroxidos = st.number_input("Índice de Peróxidos (mEq O2/Kg)", min_value=0.0, format="%.3f")
            if peroxidos >= 0:
                valores['peroxidos'] = peroxidos
        
        if analisar_ks:
            st.subheader("Parâmetros K")
            k232 = st.number_input("K232", min_value=0.0, format="%.3f")
            if k232 >= 0:
                valores['k232'] = k232
                
            k270 = st.number_input("K270", min_value=0.0, format="%.3f")
            if k270 >= 0:
                valores['k270'] = k270
                
            delta_k = st.number_input("Delta K", min_value=0.0, format="%.3f")
            if delta_k >= 0:
                valores['delta_k'] = delta_k
    
    with col2:
        if st.button("Classificar Azeite"):
            if not num_amostra:
                st.error("Por favor, insira o número da amostra.")
            elif not valores:
                st.error("Por favor, selecione pelo menos um parâmetro para análise.")
            else:
                resultado = classificar_azeite(valores)
                
                data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
                st.write(f"Data/Hora: {data_hora}")
                
                st.subheader("Resultados da Análise")
                st.write(
                    f"De acordo com a classificação presente no Anexo 1 do Regulamento Delegado (UE) 2022/2104 "
                    f"da Comissão de 29 de julho de 2022, o Azeite referente à amostra {num_amostra}, "
                    f" segundo os parâmetros físico-químicos, classifica-se como {resultado['classificacao']}"
                )
                
                st.write(f"Parâmetros analisados: {', '.join(resultado['parametros_analisados'])}")
                
                st.write("Detalhes por parâmetro:")
                resultados_tabela = []
                for param, valor in valores.items():
                    status = resultado['detalhes'].get(param, "Não avaliado")
                    resultados_tabela.append({
                        "Parâmetro": param,
                        "Valor": f"{valor:.3f}",
                        "Status": status
                    })
                st.table(resultados_tabela)

if __name__ == "__main__":
    main()