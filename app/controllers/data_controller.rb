class DataController < ApplicationController

  def index
    data = { :title => "Chelsea", :data => 'dummy data'}

    latitude   = params[:lat]
    longtitude = params[:long]
    category   = params[:cat]

    #
    # get location data
    #
    response  = HTTParty.get("http://dia.offsetdesign.co.uk/api/location/#{latitude}/#{longtitude}")
    location_data = JSON.parse(response.body)

    #
    # get crime data
    #
    response  = HTTParty.get("http://dia.offsetdesign.co.uk/api/crime?lat=#{latitude}&long=#{longtitude}")
    crime_data = JSON.parse(response.body)

    #
    # get living data
    #
    response  = HTTParty.get("http://dia.offsetdesign.co.uk/api/living?lat=#{latitude}&long=#{longtitude}")
    living_data = JSON.parse(response.body)

    #
    # get pay gap data
    #
    response  = HTTParty.get("http://dia.offsetdesign.co.uk/api/paygap?lat=#{latitude}&long=#{longtitude}")
    paygap_data = JSON.parse(response.body)

    data = {  :location   => location_data,
              :datasets   => [
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