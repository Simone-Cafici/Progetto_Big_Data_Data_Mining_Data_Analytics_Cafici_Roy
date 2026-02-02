# 📊 BIG DATA ANALYSIS: ORO & ARGENTO

## 🚀 Guida all'Uso

### 1. Crea Ambiente Virtuale

```bash
# Naviga nella cartella del progetto
cd percorso/del/progetto/BIG_DATA

# Crea l'ambiente virtuale
python -m venv venv
```

**Attiva l'ambiente** (scegli in base alla tua shell):

| Shell | Comando di Attivazione |
|-------|------------------------|
| **CMD** | `venv\Scripts\activate` |
| **PowerShell** | `.\venv\Scripts\Activate.ps1` |
| **Git Bash** | `source venv/Scripts/activate` |
| **Linux/Mac** | `source venv/bin/activate` |

### 2. Installa Dipendenze

```bash
pip install -r requirements.txt
```

### 3. Scarica i Dati

```bash
python scripts/download_data.py
```

### 4. Esegui il Notebook

1. Apri `precious_metals_analysis.ipynb` in VS Code
2. Seleziona kernel **"Python (BIG_DATA)"** in alto a destra
3. Esegui le celle con `Shift+Enter`

---

## 📚 Librerie

`pandas` · `numpy` · `matplotlib` · `yfinance` · `scikit-learn` · `statsmodels` · `ipykernel` · `seaborn`
