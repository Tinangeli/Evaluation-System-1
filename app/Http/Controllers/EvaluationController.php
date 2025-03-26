<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class EvaluationController extends Controller
{
    public function getAISummary()
    {
        $djangoApiUrl = 'http://127.0.0.1:8000/api/generate-summary/'; // Replace with your actual Django URL

        $response = Http::get($djangoApiUrl);

        if ($response->successful()) {
            return response()->json($response->json());
        } else {
            return response()->json(['error' => 'Failed to fetch summary'], 500);
        }
    }
}

