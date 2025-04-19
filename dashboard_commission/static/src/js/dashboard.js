/** @odoo-module **/
import { registry } from "@web/core/registry";
import { session } from "@web/session";
import { _t } from "@web/core/l10n/translation";
import { Component } from "@odoo/owl";
import { onWillStart, onMounted, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";
const actionRegistry = registry.category("actions");
export class SalesCommissionDashboard extends Component{
//Initializes the SalesCommissionDashboard component,

    setup() {
            super.setup(...arguments);
            this.orm = useService('orm')
            this.user = user;
            this.chartpie = null
            this.chartbar = null
            this.myChartsline = null
            this.actionService = useService("action");
            this.state = useState({
                commission_distribution : [],
                total_sale : [],
                trend_labels : [],
                trend_values: [],
                sales_team : []

            });
            // When the component is about to start, fetch data in tiles
            onWillStart(async () => {
                await this.fetch_data();
            });
            //When the component is mounted, render various charts
            onMounted(async () => {
                await this.get_dashboard_metrics();
            });
    }

    async fetch_data() {
    //  Function to fetch all the pos details
        var result = await this.orm.call('sale.order','get_dashboard_metrics',[false, false])
             this.state.total_sale = result['total_sale'],
             this.state.commission_distribution = result['commission_distribution']
             this.state.trend_labels = result['trend_labels']
             this.state.trend_values = result['trend_values']
             this.state.sales_teams = result['sales_teams']

    }

    onclick_pos_sales_team(events){
        var option = $(events.target).val();

        const startDate = $('#start_date_filter').val();
        const endDate = $('#end_date_filter').val();

       var self = this
        var self = this

//        let chartpie = null;

       var commission_distribution = $("#commission_distribution");
       var commission_distribution_graph = $(".commission_distribution_graph");
       var commission_trends = $(".sales_trend_chart");

       this.orm.call('sale.order', 'get_dashboard_metrics',[startDate, endDate, option])
        .then(function (arrays) {

          var data1 = {
            labels: arrays['commission_distribution'],
            datasets: [
              {
                label: "",
                data: arrays['commission_distribution_vals'],
                backgroundColor: [
                  "rgb(148, 22, 227)",
                  "rgba(54, 162, 235)",
                  "rgba(75, 192, 192)",
                  "rgba(153, 102, 255)",
                  "rgba(10,20,30)"
                ],
                borderColor: [
                 "rgba(255, 99, 132,)",
                  "rgba(54, 162, 235,)",
                  "rgba(75, 192, 192,)",
                  "rgba(153, 102, 255,)",
                  "rgba(10,20,30,)"
                ],
                borderWidth: 1
              },

            ]
          };
    //options
          var options1 = {
            responsive: true,
             scales: {
          x: {
            title: {
              display: true,
              text: "Achievements Pie",
              position: "top",
              fontSize: 24,
              color: "#111"
            }
          }
        },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            }
          };
          //create Chart class object


          if (window.chartpie){
            window.chartpie.destroy();
          }



          window.chartpie = new Chart(commission_distribution, {
            type: "pie",
            data: data1,
            options: options1
          });




          // -------------------//
//

            var data = {

            labels: arrays['commission_distribution'],
            datasets: [
              {
                label: "Quantity",
                data: arrays['commission_distribution_vals'],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };
    //options
          var options = {
            responsive: true,
            indexAxis: 'y',
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
             scales: {
          x: {
            title: {
              display: true,
              text: "Achievements Bar",
              position: "top",
              fontSize: 24,
              color: "#111"
            }
          }
        },
          };
          //create Chart class object



          if (window.myChartsbar != undefined){
          window.myChartsbar.destroy();
          }



          window.myChartsbar = new Chart(commission_distribution_graph, {
            type: "bar",
            data: data,
            options: options
          });








          // ----------------------//



          var data3 = {
                            labels: arrays['trend_labels'],
                            datasets: [{
                                label: 'Sales Over Time',
                                data: arrays['trend_values'],
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                tension: 0.3
                            }]
                        };
    //options
          var options3 = {
                            responsive: true,
                            plugins: {
                                legend: { display: false }
                            }
                        };
          //create Chart class object
          if (window.myChartsline != undefined)
          window.myChartsline.destroy();


          window.myChartsline = new Chart(commission_trends, {
            type: "line",
            data: {
                            labels: arrays['trend_labels'],
                            datasets: [{
                                label: 'Sales Over Time',
                                data: arrays['trend_values'],
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                tension: 0.3
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { display: false }
                            }
                        }
          });



        });
    }

    get_dashboard_metrics(){
    //      To render the top customer pie chart
       var self = this
       var commission_distribution = $("#commission_distribution");
       var commission_distribution_graph = $(".commission_distribution_graph");
       var commission_trends = $(".sales_trend_chart");

       this.orm.call('sale.order', 'get_dashboard_metrics')
        .then(function (arrays) {

          var data1 = {
            labels: arrays['commission_distribution'],
            datasets: [
              {
                label: "",
                data: arrays['commission_distribution_vals'],
                backgroundColor: [
                  "rgb(148, 22, 227)",
                  "rgba(54, 162, 235)",
                  "rgba(75, 192, 192)",
                  "rgba(153, 102, 255)",
                  "rgba(10,20,30)"
                ],
                borderColor: [
                 "rgba(255, 99, 132,)",
                  "rgba(54, 162, 235,)",
                  "rgba(75, 192, 192,)",
                  "rgba(153, 102, 255,)",
                  "rgba(10,20,30,)"
                ],
                borderWidth: 1
              },

            ]
          };
    //options
          var options1 = {
            responsive: true,
             scales: {
          x: {
            title: {
              display: true,
              text: "Achievements Pie",
              position: "top",
              fontSize: 24,
              color: "#111"
            }
          }
        },
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            }
          };
          //create Chart class object
          if (window.chartpie){
            alert("Destroyed")
            window.chartpie.destroy();
          }



          window.chartpie = new Chart(commission_distribution, {
            type: "pie",
            data: data1,
            options: options1
          });





          // -------------------//
//

            var data = {

            labels: arrays['commission_distribution'],
            datasets: [
              {
                label: "Quantity",
                data: arrays['commission_distribution_vals'],
                backgroundColor: [
                  "rgba(255, 99, 132,1)",
                  "rgba(54, 162, 235,1)",
                  "rgba(75, 192, 192,1)",
                  "rgba(153, 102, 255,1)",
                  "rgba(10,20,30,1)"
                ],
                borderColor: [
                 "rgba(255, 99, 132, 0.2)",
                  "rgba(54, 162, 235, 0.2)",
                  "rgba(75, 192, 192, 0.2)",
                  "rgba(153, 102, 255, 0.2)",
                  "rgba(10,20,30,0.3)"
                ],
                borderWidth: 1
              },

            ]
          };
    //options
          var options = {
            responsive: true,
            indexAxis: 'y',
            legend: {
              display: true,
              position: "bottom",
              labels: {
                fontColor: "#333",
                fontSize: 16
              }
            },
             scales: {
          x: {
            title: {
              display: true,
              text: "Achievements Bar",
              position: "top",
              fontSize: 24,
              color: "#111"
            }
          }
        },
          };
          //create Chart class object

          if (window.myChartsbar != undefined)
          window.myChartsbar.destroy();



          window.myChartsbar = new Chart(commission_distribution_graph, {
            type: "bar",
            data: data,
            options: options
          });







          // ----------------------//



          var data3 = {
                            labels: arrays['trend_labels'],
                            datasets: [{
                                label: 'Sales Over Time',
                                data: arrays['trend_values'],
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                tension: 0.3
                            }]
                        };
    //options
          var options3 = {
                            responsive: true,
                            plugins: {
                                legend: { display: false }
                            }
                        };
          //create Chart class object
          if (window.myChartsline != undefined){
          window.myChartsline.destroy();
          }


          window.myChartsline = new Chart(commission_trends, {
            type: "line",
            data: {
                            labels: arrays['trend_labels'],
                            datasets: [{
                                label: 'Sales Over Time',
                                data: arrays['trend_values'],
                                borderColor: 'rgba(75, 192, 192, 1)',
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                tension: 0.3
                            }]
                        },
                        options: {
                            responsive: true,
                            plugins: {
                                legend: { display: false }
                            }
                        }
          });

        });
        }

}
SalesCommissionDashboard.template = 'SalesCommissionDashboard'
registry.category("actions").add("sale_commission_order_menu", SalesCommissionDashboard)
