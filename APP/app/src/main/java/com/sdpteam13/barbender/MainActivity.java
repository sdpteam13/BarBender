package com.sdpteam13.barbender;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.InetAddress;
import java.net.Socket;
import java.net.URL;
import java.net.UnknownHostException;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.FormBody;
import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {

    public static final String TAG = MainActivity.class.getSimpleName();

    public static  String wifiModuleIp="192.168.105.142";
    public static int wifiModulePort = 53421;
    public static String CMD = "0";
    Socket myAppSocket = null;

    public static final MediaType JSON
            = MediaType.get("application/json; charset=utf-8");



   String post(String url, String command) throws IOException {
        final String[] responseResult = {""};
        OkHttpClient client = new OkHttpClient();

        RequestBody body = new FormBody.Builder()
                .add("seat",command)
                .build();
        Request request = new Request.Builder()
                .url(url)
                .post(body)
                .build();
        Call call = client.newCall(request);

        call.enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                Log.e(TAG,"Could not connect to url");
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                Log.d(TAG,"Success");
                responseResult[0] = response.body().string();
            }
        });
        return responseResult[0];
    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_seat);
        TextView result_textview = (TextView)findViewById(R.id.result_textview);

        String url = "http://192.168.105.142/APP";
        String seatnumber = getIntent().getStringExtra("Seat");
        result_textview.setText("Seat number: " + seatnumber + "\n\n I won't be long now...please feel free to order again at any time!");

        Log.d(TAG,"the seat number is: "+ seatnumber);
        try {
            post(url,seatnumber);
        }catch (IOException e){e.printStackTrace();
        Log.e(TAG, "POST DIDNT HAPPEN");}


        finish();
//        test.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {

                // Connection with sockets
//                wifiModuleIp = "192.168.105.142";
//                wifiModulePort = 53421;
//                CMD = "Go";
//                Socket_AsyncTask cmd_go = new Socket_AsyncTask();
//                cmd_go.execute();

                // Connection with flask
                /*String url = "http://192.168.105.142/APP";
                CallAPI cmd_go = new CallAPI();
                cmd_go.execute(url,"Go");*/

                // Connection with okhttp3
               // String url = "http://192.168.105.142/APP";
             //   String command = "w";
           //     try {
         //           post(url,command);
       //         }catch (IOException e){e.printStackTrace();}
     //       }
//        });

    }

    //Connection with socket
    //Helper class for TCP-IP protocol interface
    // Need to connect end send command to pi over wifi
    public class Socket_AsyncTask extends AsyncTask<Void,Void,Void>
    {
        Socket socket;

        @Override
        protected Void doInBackground(Void... params) {
            try
            {
                InetAddress inetAddress = InetAddress.getByName(MainActivity.wifiModuleIp);
                socket = new java.net.Socket(inetAddress,MainActivity.wifiModulePort);
                DataOutputStream dataOutputStream = new DataOutputStream(socket.getOutputStream());
                dataOutputStream.writeBytes(CMD);
                dataOutputStream.close();
                socket.close();
            }catch (UnknownHostException e)
            {
                e.printStackTrace();
            }catch (IOException e)
            {
                e.printStackTrace();
            }
            return null;
        }
    }

    // connection with flask
    public class CallAPI extends AsyncTask<String, String, String> {

        public CallAPI(){
            //set context variables if required
        }

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
        }

        @Override
        protected String doInBackground(String... params) {
            String urlString = params[0]; // URL to call
            Log.d(TAG,"the url is:" + urlString);
            String data = params[1]; //data to post
            Log.d(TAG,"the message is: "+ data);
            OutputStream out = null;

            try {
                URL url = new URL(urlString);
                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                out = new BufferedOutputStream(urlConnection.getOutputStream());
                Log.d(TAG,"out is: " + out);

                BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(out, "UTF-8"));
                writer.write(data);
                writer.flush();
                writer.close();
                out.close();

                urlConnection.connect();
                Log.d(TAG,"url connection is: "+ urlConnection.getURL());
            } catch (Exception e) {
                System.out.println(e.getMessage());
                Log.e(TAG,"Something went wrong: "+ e.getMessage());
                e.printStackTrace();
            }
            return null;
        }
    }

}
