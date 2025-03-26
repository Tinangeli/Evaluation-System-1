<?php

namespace App\Livewire; // ✅ Correct Livewire namespace

use Livewire\Component;
use Illuminate\Support\Facades\Http; // ✅ Make sure this is included

class Dashboard extends Component
{
    public $summary = '';

    public function fetchAISummary(): void
    {
        // ✅ Use Laravel's HTTP client properly
        $response = Http::get('http://127.0.0.1:8000/api/generate-summary/');

        if ($response->successful()) {
            $this->summary = $response->json()['summary'];
        } else {
            $this->summary = "Error fetching AI response.";
        }
    }

    public function render()
    {
        return view('livewire.dashboard');
    }
}
