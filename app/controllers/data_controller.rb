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
    # get 
    #

    respond_to do |format|
      format.json { render :json => data.merge(crime_data) }
    end
  end
end