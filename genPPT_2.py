from pptx import Presentation
from pptx.util import Inches
from pptx.enum.text import PP_ALIGN

prs = Presentation()

def add_title_content_slide(title_text, bullets=None):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    
    # Title (let PowerPoint style it)
    slide.shapes.title.text = title_text
    
    # Bullets (use default formatting)
    if bullets:
        tf = slide.placeholders[1].text_frame
        tf.text = bullets[0]   # first bullet keeps default style
        
        for bullet in bullets[1:]:
            p = tf.add_paragraph()
            p.text = bullet

    return slide


def add_blank_slide(title_text, bullets=None, image_note=None):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank
    
    # Title (minimal styling only for alignment)
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12), Inches(1.2))
    tf = title_box.text_frame
    tf.text = title_text
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    
    # Bullets (no font overrides)
    if bullets:
        content_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(7.8), Inches(5.2))
        tf = content_box.text_frame
        tf.text = bullets[0]
        
        for bullet in bullets[1:]:
            p = tf.add_paragraph()
            p.text = bullet
    
    # Image placeholder
    if image_note:
        img_box = slide.shapes.add_textbox(Inches(8.8), Inches(2.0), Inches(4.5), Inches(3.5))
        tf = img_box.text_frame
        tf.text = f"[INSERT FIGURE HERE]\n{image_note}"
    
    return slide


# ====================== 28 SLIDES ======================

# Slide 1: Title Slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = "The Intrinsic Dimensionality of the Stock Market:\nA Geometric Approach to Factor-Based Market Analysis"
subtitle.text = "B.Tech Project Report\nRohan Kumar Mahato (220101088)\nUnder the guidance of\nProf. Benny George K\nDepartment of Computer Science and Engineering\nIndian Institute of Technology Guwahati\nApril 2026"

# Slide 2: Agenda
agenda = [
    "Introduction & Motivation",
    "Contributions, Highlights & Novelty",
    "Proof of Correctness & Methodological Rigor",
    "Mathematical Foundations",
    "Data Collection & Preprocessing",
    "Research Methodology",
    "Full-Sample Empirical Results",
    "Subperiod Analysis & Temporal Evolution",
    "Economic Interpretation & Insights",
    "Scale, Extensibility & Predictive Potential",
    "Why Data Till 2020? + Limitations",
    "Conclusion, Future Work & Takeaways",
    "Q&A"
]
add_title_content_slide("Agenda", agenda)

# Slide 3: Background
bullets = [
    "One of the fastest-growing emerging equity markets",
    "NSE has over 5,000 listed companies",
    "NIFTY 500 covers approximately 93% of total market cap",
    "Diverse sectoral representation: IT, Financials, Pharma, Industrials, etc.",
    "Massive high-dimensional daily return data"
]
add_title_content_slide("Introduction – Background of the Indian Equity Market", bullets)

# Slide 4: Curse of Dimensionality
bullets = [
    "For N ≈ 400 stocks: ~80,000 unique pairwise correlations",
    "Distance concentration in high dimensions",
    "Sample covariance matrices dominated by noise",
    "Traditional statistical models frequently fail or overfit"
]
add_title_content_slide("The Curse of Dimensionality in Financial Markets", bullets)

# Slide 5: Geometric Perspective
bullets = [
    "Each trading day treated as a vector in R^N",
    "Market history forms a cloud of points in high-dimensional space",
    "Gaussian Annulus Theorem (Thin Shell Phenomenon)",
    "Real markets deviate significantly from pure randomness",
    "Indicates presence of hidden low-dimensional structure"
]
add_title_content_slide("Geometric Perspective: Markets as High-Dimensional Objects", bullets)

# Slide 6: Motivation & Objectives
bullets = [
    "Uncover the intrinsic dimensionality of the Indian equity market",
    "Build low-rank factor models separating signal from noise",
    "Analyze stability across frequencies and economic regimes",
    "Provide strong sectoral interpretability",
    "Derive practical insights for risk management and portfolio construction"
]
add_title_content_slide("Motivation & Research Objectives", bullets)

# Slide 7: Contributions & Highlights
bullets = [
    "Rigorous geometric and Random Matrix Theory foundation",
    "Fixed NIFTY 500 universe (378 stocks) – eliminates survivorship bias",
    "Multi-frequency analysis: daily, weekly, and monthly returns",
    "Temporal regime analysis across three economic subperiods",
    "Sectoral dominance analysis using loading heatmaps",
    "Demonstrates low intrinsic dimensionality with economic meaning"
]
add_title_content_slide("Main Contributions & Highlights", bullets)

# Slide 8: Novelty
bullets = [
    "Not merely repeating existing work — significant extensions made:",
    "• Fixed stock universe instead of dynamic indices",
    "• Multi-frequency + detailed subperiod evolution",
    "• Strong geometric foundation and sectoral interpretability",
    "",
    "Related Papers:",
    "• Pawanesh et al. (2024/2025) – RMT on NIFTY networks",
    "• Kulkarni et al. – Early RMT applications to Indian market"
]
add_title_content_slide("Novelty – Relation to Existing Literature", bullets)

# Slide 9: Proof of Correctness
bullets = [
    "PCA derived from first principles (variance maximization + SVD)",
    "Random Matrix Theory (Marchenko-Pastur law) for signal-noise separation",
    "Johnson-Lindenstrauss Lemma provides theoretical guarantees",
    "Results consistent across frequencies and subperiods",
    "Fixed universe + standardization reduces bias",
    "Fully transparent and reproducible pipeline"
]
add_title_content_slide("Proof of Correctness – Why Our Work is Reliable", bullets)

# Slide 10: Mathematical Foundations
bullets = [
    "From geometry to linear algebra",
    "Sample covariance matrix and eigenvalue decomposition",
    "Singular Value Decomposition (SVD)",
    "Standardization of returns (zero mean, unit variance)",
    "Low-rank approximation and factor model"
]
add_title_content_slide("Mathematical Foundations", bullets)

# Slide 11: RMT Connection
bullets = [
    "RMT distinguishes signal (large eigenvalues) from noise",
    "PC1: Strong Market Factor",
    "PC2–PC5: Sectoral and thematic rotation factors",
    "PCA preferred due to variance maximization, orthogonality, and interpretability"
]
add_title_content_slide("Connection to Random Matrix Theory", bullets)

# Slide 12: Fixed Universe
bullets = [
    "Based on NIFTY 500 membership as of end of 2004",
    "Final cleaned universe: 378 stocks",
    "Eliminates survivorship bias for reliable long-term analysis",
    "Robust ticker mapping using NSE + Yahoo Finance"
]
add_title_content_slide("Data Collection – Fixed NIFTY 500 Universe", bullets)

# Slide 13: Preprocessing
bullets = [
    "Historical adjusted close prices from yfinance (2005–2020)",
    "Missing value imputation using forward-fill + backward-fill",
    "Return calculation at three frequencies: daily, weekly, monthly",
    "Standardization applied to each stock individually",
    "Final dataset: ~3,720 trading days × 378 stocks"
]
add_title_content_slide("Preprocessing & Dataset Characteristics", bullets)

# Slide 14: Methodology
bullets = [
    "Standardize returns → Compute correlation matrix → Apply PCA",
    "Multi-frequency and multi-regime (subperiod) analysis",
    "Sector-wise loading analysis using average absolute loadings",
    "Visualization via scree plots, cumulative variance, and heatmaps"
]
add_title_content_slide("Research Methodology Overview", bullets)

# Slide 15: Full-Sample Results
bullets = [
    "Scree plots (linear and log scale)",
    "Strong decay after first few principal components",
    "Cumulative variance explained by top components"
]
add_blank_slide("Full-Sample Empirical Results – Eigenvalue Analysis", bullets, "Fig 5.1 - 5.5: Scree plots & Cumulative Variance")

# Slide 16: Full-Sample Heatmaps
bullets = [
    "Stock-level loading heatmaps",
    "Sectoral dominance heatmaps across frequencies",
    "Clear market factor (PC1) and sectoral patterns"
]
add_blank_slide("Full-Sample – Loading & Sectoral Dominance Heatmaps", bullets, "Fig 5.6 - 5.11")

# Slide 17: Subperiod Definition
bullets = [
    "2005–2010: Crisis-driven market (Global Financial Crisis)",
    "2010–2015: Transition and recovery period",
    "2015–2020: Reform period and early COVID impact"
]
add_title_content_slide("Subperiod Analysis – Definition & Economic Context", bullets)

# Slide 18: Subperiod Eigenvalue Results
bullets = [
    "Comparative scree plots across subperiods",
    "Cumulative variance explained",
    "Number of significant components remains low"
]
add_blank_slide("Subperiod Results – Eigenvalue Analysis", bullets, "Fig 6.1 - 6.4")

# Slide 19: Subperiod Sectoral Evolution
bullets = [
    "Sectoral dominance heatmaps for each subperiod",
    "Evolution of factor structure over time",
    "Persistent market factor with changing sectoral influence"
]
add_blank_slide("Subperiod – Sectoral Evolution", bullets, "Fig 6.5 - 6.7")

# Slide 20: Economic Interpretation
bullets = [
    "PC1: Dominant Market Factor representing overall economic conditions",
    "PC2–PC5: Sectoral and thematic rotation factors",
    "Factors are economically meaningful and robust",
    "Clear mapping between statistical components and real market drivers"
]
add_title_content_slide("Economic Interpretation of Principal Components", bullets)

# Slide 21: Key Insights
bullets = [
    "Indian equity market exhibits low intrinsic dimensionality",
    "Structure evolves with economic regimes but remains interpretable",
    "Strong robustness across frequencies and subperiods",
    "Useful for risk management, factor investing, and regime detection"
]
add_title_content_slide("Key Market Insights & Robustness", bullets)

# Slide 22: Scale of Study
bullets = [
    "Fixed universe: 378 stocks",
    "Time span: 15+ years (≈ 3,720 trading days)",
    "Total data points: ~1.4 million (daily)",
    "Comprehensive analysis: full-sample + 3 subperiods × 3 frequencies"
]
add_title_content_slide("Scale of This Study", bullets)

# Slide 23: Extensibility
bullets = [
    "Highly extensible framework:",
    "• Extend dataset beyond 2020",
    "• Incorporate non-linear methods (autoencoders, VAEs)",
    "• Develop dynamic/time-varying factor models",
    "• Integrate with machine learning for prediction",
    "• Apply to other markets and asset classes"
]
add_title_content_slide("Extensibility of the Work", bullets)

# Slide 24: Predictive Potential
bullets = [
    "Descriptive and explanatory model (uncovers hidden factors)",
    "Not designed as a direct price predictor",
    "Low-rank approximation useful for denoising and risk estimation",
    "Extracted factors can serve as powerful features in forecasting models",
    "Limitation: Markets are non-stationary and driven by new information"
]
add_title_content_slide("Predictive Potential – Can It Predict Future Prices?", bullets)

# Slide 25: Why Till 2020
bullets = [
    "Project timeline and need for a clean, consistent 15-year window",
    "Covers major economic regimes (crisis, recovery, pre-COVID)",
    "Fixed-universe construction more reliable up to 2020",
    "Avoids contamination from extreme post-2020 events",
    "Easily extendable to 2025 in future research"
]
add_title_content_slide("Why Dataset Only Till 2020?", bullets)

# Slide 26: Limitations
bullets = [
    "Fixed universe misses companies listed after 2004",
    "PCA assumes linear relationships",
    "Dataset ends in 2020",
    "Typical data quality challenges in emerging markets"
]
add_title_content_slide("Limitations of the Study", bullets)

# Slide 27: Conclusion
bullets = [
    "Indian equity market has low intrinsic dimensionality",
    "Dominated by a strong market factor + few sectoral factors",
    "Fixed-universe + multi-frequency + RMT approach is effective",
    "Geometric perspective reveals hidden order in market data"
]
add_title_content_slide("Conclusion & Main Takeaways", bullets)

# Slide 28: Thank You
bullets = [
    "Future Work:",
    "   • Extend dataset to 2025 and beyond",
    "   • Non-linear dimensionality reduction",
    "   • Dynamic factor models and ML integration",
    "",
    "Thank You!",
    "I welcome your questions"
]
add_title_content_slide("Future Work & Thank You", bullets)

# ====================== SAVE ======================
prs.save("BTP_Thesis_Intrinsic_Dimensionality_28_Slides.pptx")

print("✅ Successfully generated: BTP_Thesis_Intrinsic_Dimensionality_28_Slides.pptx")
print("Open the file in PowerPoint.")
print("Replace the image placeholders with actual figures from your report (scree plots, heatmaps, pipeline, sector pie chart, etc.).")
print("Recommended: Apply a professional theme with blue/saffron colors.")