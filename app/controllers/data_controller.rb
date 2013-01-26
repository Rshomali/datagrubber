class DataController < ApplicationController

  def index
    data = { :title => "Chelsea", :data => 'dummy data'}

    latitude   = params[:lat]
    longtitude = params[:long]
    category   = params[:cat]

    #
    # get crime data
    #
    response  = HTTParty.get('http://dia.offsetdesign.co.uk/api/crime?lat=xxx&long=yyy')
    crime_data = JSON.parse(response.body)

    #
    # get living data
    #
    response  = HTTParty.get('http://dia.offsetdesign.co.uk/api/living?lat=xxx&long=yyy')
    living_data = JSON.parse(response.body)

    #
    # get pay gap data
    #
    response  = HTTParty.get('http://dia.offsetdesign.co.uk/api/paygap?lat=xxx&long=yyy')
    paygap_data = JSON.parse(response.body)

    data = { :title => "Shoreditch"
             :datasets => [
                            crime_data,
                            living_data,
                            paygap_data
                          ]
          }

    respond_to do |format|
      format.json { render :json => data }
    end
  end
end