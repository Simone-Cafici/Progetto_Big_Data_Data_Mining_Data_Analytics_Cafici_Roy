#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
=============================================================================
SCRIPT DI ACQUISIZIONE DATI - ORO, ARGENTO, S&P500, VIX
=============================================================================

Questo script scarica i prezzi storici di:
- Oro e Argento (FUTURES - GC=F, SI=F)
- S&P 500 (Indice azionario - ^GSPC)
- VIX (Indice volatilità - ^VIX)

utilizzando l'API di Yahoo Finance. I dati vengono salvati in formato CSV 
per l'analisi successiva nel notebook.

Lo script esegue 4 FASI per dimostrare il processo di acquisizione dati:
- FASE 1: Tentativo download valori SPOT (fallisce - non disponibili)
- FASE 2: Download Futures Oro/Argento (unica fonte gratuita disponibile)
- FASE 3: Download S&P500 e VIX (variabili indipendenti per regressione)
- FASE 4: Merge e salvataggio dataset completo

La pulizia dei rollover gaps viene effettuata nel notebook per documentare
il processo di Data Cleaning durante la presentazione.

Autore: Data Science Project - Big Data Analysis
Data: Gennaio 2026
=============================================================================
"""

import os
import sys
from datetime import datetime
import pandas as pd
import yfinance as yf


def scarica_dati_metalli(data_inizio: str = "2000-01-01", 
                         data_fine: str = None,
                         cartella_output: str = "data") -> pd.DataFrame:
    """
    Scarica i dati storici di Oro, Argento, S&P500 e VIX da Yahoo Finance.
    
    Esegue 4 FASI per documentare il processo di acquisizione:
    FASE 1: Tentativo download SPOT (ideale ma non disponibile)
    FASE 2: Download Futures Oro/Argento (unica fonte disponibile gratuitamente)
    FASE 3: Download S&P500 e VIX (variabili indipendenti)
    FASE 4: Merge e salvataggio dataset completo
    
    Args:
        data_inizio: Data iniziale in formato 'YYYY-MM-DD' (default: 2000-01-01)
        data_fine: Data finale (default: oggi)
        cartella_output: Cartella dove salvare il CSV
        
    Returns:
        DataFrame con prezzi di chiusura Oro, Argento, S&P500, VIX (dati grezzi)
    """
    
    if data_fine is None:
        data_fine = datetime.now().strftime("%Y-%m-%d")
    
    print("=" * 70)
    print("ACQUISIZIONE DATI: ORO, ARGENTO, S&P500, VIX")
    print("=" * 70)
    print(f"Periodo richiesto: {data_inizio} → {data_fine}")
    print()
    
    # ==========================================================================
    # FASE 1: Tentativo download valori SPOT
    # ==========================================================================
    print("╔" + "═" * 68 + "╗")
    print("║ FASE 1: Tentativo download valori SPOT                            ║")
    print("║ (Prezzo 'qui e ora' del metallo fisico - ideale per analisi)      ║")
    print("╚" + "═" * 68 + "╝")
    
    ticker_oro_spot = "XAUUSD=X"
    ticker_argento_spot = "XAGUSD=X"
    
    try:
        oro_spot = yf.download(ticker_oro_spot, start=data_inizio, end=data_fine, 
                               progress=False, auto_adjust=True)
        argento_spot = yf.download(ticker_argento_spot, start=data_inizio, end=data_fine,
                                   progress=False, auto_adjust=True)
        
        if len(oro_spot) == 0:
            print(f"    ❌ Oro SPOT ({ticker_oro_spot}): Non disponibile")
        else:
            print(f"    ✓ Oro SPOT: {len(oro_spot)} record")
            
        if len(argento_spot) == 0:
            print(f"    ❌ Argento SPOT ({ticker_argento_spot}): Non disponibile")
        else:
            print(f"    ✓ Argento SPOT: {len(argento_spot)} record")
            
    except Exception as e:
        print(f"    ❌ Errore: I ticker SPOT non sono disponibili su Yahoo Finance")
        oro_spot = pd.DataFrame()
        argento_spot = pd.DataFrame()
    
    print("\n    💡 I mercati Spot sono OTC - dati storici non disponibili gratuitamente\n")
    
    # ==========================================================================
    # FASE 2: Download dati FUTURES
    # ==========================================================================
    print("╔" + "═" * 68 + "╗")
    print("║ FASE 2: Download FUTURES (unica fonte gratuita disponibile)       ║")
    print("║ Ticker: GC=F (Oro) e SI=F (Argento) - Borsa COMEX                 ║")
    print("╚" + "═" * 68 + "╝")
    
    ticker_oro_futures = "GC=F"
    ticker_argento_futures = "SI=F"
    
    try:
        oro_futures = yf.download(ticker_oro_futures, start=data_inizio, end=data_fine,
                                  progress=False, auto_adjust=True)
        argento_futures = yf.download(ticker_argento_futures, start=data_inizio, end=data_fine,
                                      progress=False, auto_adjust=True)
        
        print(f"    ✓ Oro Futures (GC=F): {len(oro_futures)} record")
        print(f"    ✓ Argento Futures (SI=F): {len(argento_futures)} record")
        
        if len(oro_futures) > 0:
            print(f"    📅 Primo record: {oro_futures.index.min().strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"    ❌ Errore download Futures: {e}")
        oro_futures = pd.DataFrame()
        argento_futures = pd.DataFrame()
    
    print("\n    ⚠️ Yahoo Finance: dati disponibili solo da agosto 2000\n")
    
    # ==========================================================================
    # FASE 3: Download S&P500 e VIX
    # ==========================================================================
    print("╔" + "═" * 68 + "╗")
    print("║ FASE 3: Download S&P500 e VIX (variabili indipendenti)            ║")
    print("║ Ticker: ^GSPC (S&P500) e ^VIX (Indice Volatilità)                 ║")
    print("╚" + "═" * 68 + "╝")
    
    ticker_sp500 = "^GSPC"
    ticker_vix = "^VIX"
    
    try:
        sp500 = yf.download(ticker_sp500, start=data_inizio, end=data_fine,
                            progress=False, auto_adjust=True)
        vix = yf.download(ticker_vix, start=data_inizio, end=data_fine,
                          progress=False, auto_adjust=True)
        
        print(f"    ✓ S&P 500 (^GSPC): {len(sp500)} record")
        print(f"    ✓ VIX (^VIX): {len(vix)} record")
        
    except Exception as e:
        print(f"    ❌ Errore download S&P500/VIX: {e}")
        sp500 = pd.DataFrame()
        vix = pd.DataFrame()
    
    print("\n    💡 S&P500: Indice azionario USA (risk-on indicator)")
    print("    💡 VIX: Indice volatilità, 'fear gauge' del mercato\n")
    
    # ==========================================================================
    # FASE 4: Merge e salvataggio dataset completo
    # ==========================================================================
    print("╔" + "═" * 68 + "╗")
    print("║ FASE 4: Merge dataset completo                                    ║")
    print("║ Colonne: Gold_USD, Silver_USD, SP500, VIX                         ║")
    print("╚" + "═" * 68 + "╝")
    
    def estrai_close(df):
        """Estrae la colonna Close gestendo MultiIndex."""
        if df.empty:
            return pd.Series(dtype=float)
        if isinstance(df.columns, pd.MultiIndex):
            return df['Close'].iloc[:, 0]
        return df['Close']
    
    # Estrai prezzi di chiusura
    oro_close = estrai_close(oro_futures)
    argento_close = estrai_close(argento_futures)
    sp500_close = estrai_close(sp500)
    vix_close = estrai_close(vix)
    
    # Crea DataFrame finale (DATI GREZZI - pulizia nel notebook)
    df = pd.DataFrame({
        'Gold_USD': oro_close,
        'Silver_USD': argento_close,
        'SP500': sp500_close,
        'VIX': vix_close
    })
    
    # Rimuovi righe completamente vuote
    df = df.dropna(how='all')
    
    # Ordina per data
    df = df.sort_index()
    
    print(f"    ✅ Dataset finale: {len(df)} record (dati grezzi)")
    print(f"    📅 Periodo: {df.index.min().strftime('%Y-%m-%d')} → {df.index.max().strftime('%Y-%m-%d')}")
    print(f"    📊 Valori mancanti Oro: {df['Gold_USD'].isna().sum()}")
    print(f"    📊 Valori mancanti Argento: {df['Silver_USD'].isna().sum()}")
    print(f"    📊 Valori mancanti S&P500: {df['SP500'].isna().sum()}")
    print(f"    📊 Valori mancanti VIX: {df['VIX'].isna().sum()}")
    
    # ==========================================================================
    # SALVATAGGIO
    # ==========================================================================
    os.makedirs(cartella_output, exist_ok=True)
    percorso_file = os.path.join(cartella_output, "precious_metals_data.csv")
    
    df.to_csv(percorso_file)
    print(f"\n✅ Dati salvati in: {percorso_file}")
    print(f"   Dimensione file: {os.path.getsize(percorso_file) / 1024:.1f} KB")
    
    return df


def main():
    """Funzione principale per esecuzione da riga di comando."""
    
    # Configurazione
    DATA_INIZIO = "2000-01-01"
    DATA_FINE = "2026-01-28"
    CARTELLA = "data"
    
    # Se lo script è chiamato dalla cartella scripts/, torniamo indietro
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if os.path.basename(script_dir) == "scripts":
        os.chdir(os.path.dirname(script_dir))
    
    print("\n" + "=" * 70)
    print("    BIG DATA PROJECT: ORO, ARGENTO, S&P500, VIX (2000-2026)")
    print("=" * 70 + "\n")
    
    try:
        df = scarica_dati_metalli(DATA_INIZIO, DATA_FINE, CARTELLA)
        
        print("\n" + "-" * 70)
        print("ANTEPRIMA DATI (grezzi - pulizia nel notebook):")
        print("-" * 70)
        print(df.head(10))
        print("\n... ultimi record ...")
        print(df.tail(5))
        
        print("\n" + "=" * 70)
        print("✅ ACQUISIZIONE COMPLETATA!")
        print("   Proseguire con il notebook per pulizia e analisi")
        print("=" * 70 + "\n")
        
    except Exception as e:
        print(f"\n❌ ERRORE FATALE: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
