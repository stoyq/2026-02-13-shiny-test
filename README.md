Test shiny dashboard

``` mermaid
flowchart TD
  A[/year_range/] --> F{{filtered_df}}
  B[/region/] --> F
  C[/basis_record/] --> F
  A --> VB3([vb_status])
  F --> VB1([vb_total_obs])
  F --> VB2([vb_first_recorded])
  F --> VB3([vb_status])
  F --> P1([plot_timeseries])
  F --> P2([plot_basis])
  F --> P3([map])
```
