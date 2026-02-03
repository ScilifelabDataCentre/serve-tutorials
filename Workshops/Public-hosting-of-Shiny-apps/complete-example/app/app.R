library(shiny)
library(dplyr)
library(ggplot2)
library(scales)
library(readr)

calidris_observations <- read_csv("calidris_observations.csv", locale = locale(encoding = "UTF-8"))

# Define ui
ui <- fluidPage(
  titlePanel("Number of observations of six sandpiper species over time, as recorded in the GBIF occurrences database"),
  sidebarLayout(
    sidebarPanel(
      sliderInput("yearRange", "Select year range:",
                  min = 1829, max = 2025, sep = "", value = c(1990, 2025)),
      selectInput(
        "selectedCountry",
        "Select country:",
        choices = sort(unique(calidris_observations$country_name)),
        selected = "Sweden"
      ),
      checkboxGroupInput(
        "selectedSpecies",
        "Select species:",
        choices = unique(calidris_observations$species),
        selected = "Calidris alpina"
      )
    ),
    mainPanel(
      plotOutput("observationsPlot")
    )
  ),
  fluidRow(
    column(12,
           h4("Data behind this application", style = "margin-top: 30px;"),
           HTML("<p>This dashboard is based on open data downloaded from <a href='https://gbif.org'>GBIF</a>, dataset DOI: <a href='https://doi.org/10.15468/dl.4pfamv'>https://doi.org/10.15468/dl.4pfamv</a>. It visualizes the number of reports of observation of specific species in the wild.</p>"),
           HTML("<p>The dataset contains 664,581 records of which 443k were reported through <a href='https://www.artportalen.se/'>Artportalen</a>, 128k were reported through the Norwegian Species Observation Service.</p>"),
           HTML("<p>The data includes only records with the following <i>BasisOfRecord</i>: <i>Observation, Human Observation, Occurrence evidence, Living Specimen, Machine Observation</i>. The data includes only records with the following <i>TaxonKey</i>: <i>Calidris alpina schinzii, Calidris alpina alpina, Calidris temminckii, Calidris minuta, Calidris ferruginea, Calidris ferruginea, Calidris maritima, Calidris alba</i>. Entries with no <i>Year</i> information were removed.</p>"),
           h4("Code behind this application", style = "margin-top: 30px;"),
           HTML("<p>This dashboard was created using the R Shiny framework. The code behind this dashboard can be found on Github: [XXX]. It is distributed with an MIT License.</p>"),
           h4("Photos", style = "margin-top: 30px;"),
           HTML('
                <div style="
                  display: flex;
                  flex-wrap: wrap;
                  gap: 16px;
                  align-items: flex-start;
                  margin-top: 10px;
                ">
                
                  <div style="flex: 1 1 360px; max-width: 400px; text-align: center;">
                    <img src="https://api.gbif.org/v1/image/cache/occurrence/4405543393/media/6029032fb6af7061ad789570b3e4eac5" 
                    alt="Calidris temminckii. Observed in Sweden by lappuggla (licensed under CC BY-NC 4.0" 
                    style="width: 100%; height: auto; display: block;">
                    <div style="font-size: 10px; line-height: 1.2; margin-top: 4px;"><i>Calidris temminckii</i>. <a href="https://www.gbif.org/occurrence/4405543393">Observed</a> in Sweden by lappuggla (licensed under CC BY-NC 4.0).</div>
                  </div>
                
                  <div style="flex: 1 1 360px; max-width: 400px; text-align: center;">
                    <img src="https://api.gbif.org/v1/image/cache/occurrence/5938514812/media/b7b604344f61e3212c81f4ccb6e3cea3" 
                    alt="Calidris maritima. Observed in Sweden by Janne Asp (licensed under CC BY-NC-ND 4.0" 
                    style="width: 100%; height: auto; display: block;">
                    <div style="font-size: 10px; line-height: 1.2; margin-top: 4px;"><i>Calidris maritima</i>. <a href="https://www.gbif.org/occurrence/5938514812">Observed</a> in Sweden by Janne Asp (licensed under CC BY-NC-ND 4.0).</div>
                  </div>
                  
                  <div style="flex: 1 1 360px; max-width: 400px; text-align: center;">
                    <img src="https://api.gbif.org/v1/image/cache/occurrence/4080540165/media/d026a0bb6af0a4d7343750fac4de0522" 
                    alt="Calidris minuta. Observed in Sweden by lappuggla (licensed under CC BY-NC 4.0" 
                    style="width: 100%; height: auto; display: block;">
                    <div style="font-size: 10px; line-height: 1.2; margin-top: 4px;"><i>Calidris minuta</i>. <a href="https://www.gbif.org/occurrence/4080540165">Observed</a> in Sweden by lappuggla (licensed under CC BY-NC 4.0).</div>
                  </div>
                
                  <div style="flex: 1 1 360px; max-width: 400px; text-align: center;">
                    <img src="https://api.gbif.org/v1/image/cache/occurrence/5293251518/media/3ab36b703347b7a1b4a33fe67bf413de" 
                    alt="Calidris ferruginea. Observed in Sweden by lappuggla van der Vegt (licensed under CC BY-NC 4.0" 
                    style="width: 100%; height: auto; display: block;">
                    <div style="font-size: 10px; line-height: 1.2; margin-top: 4px;"><i>Calidris ferruginea</i>. <a href="https://www.gbif.org/occurrence/5293251518">Observed</a> in Sweden by lappuggla (licensed under CC BY-NC 4.0).</div>
                  </div>

                  <div style="flex: 1 1 360px; max-width: 400px; text-align: center;">
                    <img src="https://api.gbif.org/v1/image/cache/occurrence/4926384612/media/14118f79ac4959ad1d51890518a69070" 
                    alt="Calidris alba. Observed in Sweden by Sven Gippner (licensed under CC BY-NC 4.0" 
                    style="width: 100%; height: auto; display: block;">
                    <div style="font-size: 10px; line-height: 1.2; margin-top: 4px;"><i>Calidris alba</i>. <a href="https://www.gbif.org/occurrence/4926384612">Observed</a> in Sweden by Sven Gippner (licensed under CC BY-NC 4.0).</div>
                  </div>
                  
                  <div style="flex: 1 1 360px; max-width: 400px; text-align: center;">
                    <img src="https://api.gbif.org/v1/image/cache/occurrence/5230910854/media/cd798605e8281bba67e25836b0803d99" 
                    alt="Calidris alpina. Observed in Sweden by lappuggla (licensed under CC BY-NC 4.0" 
                    style="width: 100%; height: auto; display: block;">
                    <div style="font-size: 10px; line-height: 1.2; margin-top: 4px;"><i>Calidris alpina</i>. <a href="https://www.gbif.org/occurrence/5230910854">Observed</a> in Sweden by lappuggla (licensed under CC BY-NC 4.0).</div>
                  </div>
                  
                </div>
                <br><br>
                ')
    )
  )
)

# Define server
server <- function(input, output) {
  filtered_data <- reactive({
    # Country filter
    data1 <- calidris_observations %>%
      filter(
        country_name == input$selectedCountry,
        year >= input$yearRange[1],
        year <= input$yearRange[2],
        species %in% input$selectedSpecies
      ) %>%
      mutate(country_group = input$selectedCountry)
    
    data1
  })
  
  output$observationsPlot <- renderPlot({
    ggplot(filtered_data(), aes(x = year, y = n_observations, color = species, linetype = country_group)) +
      geom_line(linewidth = 1.3) +
      scale_y_continuous(labels = label_comma()) +
      scale_x_continuous(breaks = scales::breaks_pretty()) +
      labs(
        x = "Year",
        y = "Observations",
        color = "Species",
        linetype = "Country"
      ) +
      theme_linedraw() +
      theme(
        axis.title = element_text(size = 14),
        axis.text = element_text(size = 12),
        legend.text = element_text(size = 12),
        legend.title = element_text(size = 14)
      ) +
      scale_color_viridis_d(option = "D")  # use the viridis color palette
  })
}

# Run the app
shinyApp(ui = ui, server = server)