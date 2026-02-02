library(shiny)
library(dplyr)
library(ggplot2)
library(scales)
library(readr)

calidris_observations <- read_csv("calidris_observations.csv", locale = locale(encoding = "UTF-8"))

# Define ui
ui <- fluidPage(
  titlePanel("Number of observations of [XXXXX] in the GBIF occurences database"),
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
           HTML("<p>This dashboard was created using the R Shiny framework. The code behind this dashboard can be found on Github: [XXX]. It is distributed with an MIT License.</p>")
           
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