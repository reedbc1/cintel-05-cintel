import plotly.express as px
import seaborn as sns
from shiny import reactive, render, req
from shiny.express import input, ui
from shinywidgets import render_plotly
from shinywidgets import render_widget
import palmerpenguins

# Use the built-in function to load the Palmer Penguins dataset
penguins = palmerpenguins.load_penguins()

ui.page_opts(title="Penguin Data - Brendan", fillable=True)

# sidebar
with ui.sidebar(bg="#f8f8f8", open='open'):
    ui.h2("Sidebar")
    ui.input_selectize("selected_attribute", "Selected_attribute",
                       ["bill_length_mm", "bill_depth_mm", 
                        "flipper_length_mm", "body_mass_g"])
    ui.input_numeric("plotly_bin_count", "Plotly_bin_count", 50)
    ui.input_slider("seaborn_bin_count", "Seaborn_bin_count", 1, 100, 50)
    ui.input_checkbox_group("selected_species_list", "Selected_species_list", 
                            ["Adelie", "Gentoo", "Chinstrap"], 
                            selected = ["Adelie", "Gentoo", "Chinstrap"], inline = False)
    ui.input_checkbox_group("selected_island_list", "Selected_island_list", 
                            ['Torgersen', 'Biscoe', 'Dream'], 
                            selected = ['Torgersen', 'Biscoe', 'Dream'], inline = False)
    ui.hr()
    ui.a("GitHub", href = "https://github.com/reedbc1/cintel-02-data/tree/main", target = "_blank")


# create two columns
with ui.layout_columns():
    
    # show data
    with ui.navset_card_pill(id="tab1"):  
        with ui.nav_panel("Data Table"):
            @render.data_frame  
            def penguins_data_table():
                return render.DataTable(penguins)
        with ui.nav_panel("Data Grid"):
            @render.data_frame  
            def penguins_data_grid():
                return render.DataGrid(penguins)
                
    # show graphs
    with ui.navset_card_pill(id="tab2"):  
        
        with ui.nav_panel("Plotly Histogram"):
            @render_widget  
            def plot_hist():  
                mass_fig = px.histogram(
                    data_frame=filtered_data(),
                    x=input.selected_attribute(),
                    color = "species",
                    nbins=input.plotly_bin_count(),
                ).update_layout(
                    title={"text": "Penguin Stats", "x": 0.5},
                    yaxis_title="Count",
                    xaxis_title=input.selected_attribute(),
                )
                return mass_fig
        
        with ui.nav_panel("Seaborn Histogram"):
            @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")  
            def plot():  
                ax = sns.histplot(data=filtered_data(), x="body_mass_g", 
                                  hue = "species", bins=input.seaborn_bin_count())  
                ax.set_title("Palmer Penguins")
                ax.set_xlabel("Mass (g)")
                ax.set_ylabel("Count")
                return ax 

        with ui.nav_panel("Scatterplot"):
            @render_widget  
            def plot_scatter():  
                plotly_fig = px.scatter(
                    data_frame=filtered_data(),
                    x="body_mass_g",
                    color = "species"
                ).update_layout(
                    title={"text": "Penguin Mass", "x": 0.5},
                    yaxis_title="Count",
                    xaxis_title="Body Mass (g)",
                )
    
                return plotly_fig  

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

@reactive.calc
def filtered_data():
    req(input.selected_species_list())
    req(input.selected_island_list())
    
    isSpeciesMatch = penguins["species"].isin(input.selected_species_list())
    isIslandMatch = penguins["island"].isin(input.selected_island_list())
    filtered_df_and = penguins[isSpeciesMatch & isIslandMatch]
    return filtered_df_and
