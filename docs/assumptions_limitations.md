# Assumptions and Limitations

## Key Assumptions:
1. **Temporal Correlation Implies Potential Causality**: We assume that proximity in time between an event and a price change suggests potential causality
2. **Market Efficiency**: Oil prices quickly incorporate all available information
3. **Event Isolation**: Major events have distinct temporal signatures that can be separated
4. **Data Quality**: Historical price data is accurate and complete

## Major Limitations:
1. **Correlation ≠ Causation**: Detected change points coinciding with events doesn't prove causation
2. **Confounding Variables**: Multiple simultaneous events can obscure individual impacts
3. **Data Granularity**: Daily data may miss intraday volatility around events
4. **Model Simplicity**: Single change point model may oversimplify complex market dynamics
5. **Event Selection Bias**: Researcher-selected events may miss important but less-publicized events

## Statistical vs Causal Interpretation:
- **Statistical Correlation**: We can identify when price patterns change significantly
- **Causal Impact**: Requires controlled experiments or more sophisticated causal inference methods
- **Inference Caution**: Our analysis suggests associations, not proven causal relationships